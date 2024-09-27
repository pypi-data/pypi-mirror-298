import copy
from itertools import chain
from threading import Lock, Timer
from typing import Callable, Optional, Iterable
import numpy as np

from AnyQt.QtGui import QColor, QPainter, QPen
from AnyQt.QtCore import QModelIndex, Qt, QLineF, QSortFilterProxyModel
from AnyQt.QtWidgets import QTableView, QHeaderView, \
    QStyleOptionViewItem, QApplication, QStyle, QLineEdit

from orangecontrib.prototypes.ranktablemodel import RankModel
from orangecontrib.prototypes.interactions import InteractionScorer

from Orange.data import Table, Domain, Variable
from Orange.preprocess import Discretize, Remove
from Orange.widgets import gui
from Orange.widgets.widget import OWWidget, AttributeList, Msg
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.utils.concurrents import ConcurrentWidgetMixin, TaskState
from Orange.widgets.utils.itemmodels import DomainModel
from Orange.widgets.settings import Setting, ContextSetting, DomainContextHandler
from orangecontrib.prototypes.i18n_config import *

def __(key):
    return i18n.t('prototypes.owinteractions.' + key)



class ModelQueue:
    def __init__(self):
        self.mutex = Lock()
        self.queue = []
        self.latest_state = None

    def put(self, row, state):
        with self.mutex:
            self.queue.append(row)
            self.latest_state = state

    def get(self):
        with self.mutex:
            queue, self.queue = self.queue, []
            state, self.latest_state = self.latest_state, None
        return queue, state


def run(compute_score: Callable, row_for_state: Callable,
        iterate_states: Callable, saved_state: Optional[Iterable],
        progress: int, state_count: int, task: TaskState):
    """
    Replaces ``run_vizrank``, with some minor adjustments.
        - ``ModelQueue`` replaces ``queue.Queue``
        - `row_for_state` can be called here, assuming we are not adding `Qt` objects to the model
        - `scores` removed
    """
    task.set_status(__("get_combinations"))
    task.set_progress_value(0.1)
    states = iterate_states(saved_state)

    task.set_status(__("get_scores"))
    queue = ModelQueue()
    can_set_partial_result = True

    def do_work(st, next_st):
        try:
            score = compute_score(st)
            if score is not None:
                queue.put(row_for_state(score, st), next_st)
        except Exception:
            pass

    def reset_flag():
        nonlocal can_set_partial_result
        can_set_partial_result = True

    state = None
    next_state = next(states)
    try:
        while True:
            if task.is_interruption_requested():
                return queue.get()
            task.set_progress_value(progress * 100 // state_count)
            progress += 1
            state = copy.copy(next_state)
            next_state = copy.copy(next(states))
            do_work(state, next_state)
            # for simple scores (e.g. correlations widget) and many feature
            # combinations, the 'partial_result_ready' signal (emitted by
            # invoking 'task.set_partial_result') was emitted too frequently
            # for a longer period of time and therefore causing the widget
            # being unresponsive
            if can_set_partial_result:
                task.set_partial_result(queue.get())
                can_set_partial_result = False
                Timer(0.05, reset_flag).start()
    except StopIteration:
        do_work(state, None)
        task.set_partial_result(queue.get())
    return queue.get()


class Heuristic:
    RANDOM, INFO_GAIN = 0, 1
    mode = {RANDOM: __("random_search"),
            INFO_GAIN: __("low_information_gain_first")}

    def __init__(self, weights, mode=RANDOM):
        self.n_attributes = len(weights)
        self.attributes = np.arange(self.n_attributes)
        if mode == Heuristic.INFO_GAIN:
            self.attributes = self.attributes[np.argsort(weights)]
        else:
            np.random.shuffle(self.attributes)

    def generate_states(self):
        # prioritize two mid ranked attributes over highest first
        for s in range(1, self.n_attributes * (self.n_attributes - 1) // 2):
            for i in range(max(s - self.n_attributes + 1, 0), (s + 1) // 2):
                yield self.attributes[i], self.attributes[s - i]

    def get_states(self, initial_state):
        states = self.generate_states()
        if initial_state is not None:
            while next(states) != initial_state:
                pass
            return chain([initial_state], states)
        return states


class InteractionItemDelegate(gui.TableBarItem):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: QModelIndex) -> None:
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        widget = option.widget
        style = QApplication.style() if widget is None else widget.style()
        pen = QPen(QColor("#46befa"), 5, Qt.SolidLine, Qt.RoundCap)
        line = QLineF()
        self.__style = style
        text = opt.text
        opt.text = ""
        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, widget)
        textrect = style.subElementRect(
            QStyle.SE_ItemViewItemText, opt, widget)

        interaction = self.cachedData(index, Qt.EditRole)
        # only draw bars for first column
        if index.column() == 0 and interaction is not None:
            rect = option.rect
            pw = self.penWidth
            textoffset = pw + 2
            baseline = rect.bottom() - textoffset / 2
            origin = rect.left() + 3 + pw / 2  # + half pen width for the round line cap
            width = rect.width() - 3 - pw

            def draw_line(start, length):
                line.setLine(origin + start, baseline, origin + start + length, baseline)
                painter.drawLine(line)

            scorer = index.model().scorer
            attr1 = self.cachedData(index.siblingAtColumn(2), Qt.EditRole)
            attr2 = self.cachedData(index.siblingAtColumn(3), Qt.EditRole)
            l_bar = scorer.normalize(scorer.information_gain[int(attr1)])
            r_bar = scorer.normalize(scorer.information_gain[int(attr2)])
            # negative information gains stem from issues in interaction
            # calculation and may cause bars reaching out of intended area
            l_bar, r_bar = width * max(l_bar, 0), width * max(r_bar, 0)
            interaction *= width

            pen.setWidth(pw)
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            draw_line(0, l_bar)
            draw_line(l_bar + interaction, r_bar)
            pen.setColor(QColor("#aaf22b") if interaction >= 0 else QColor("#ffaa7f"))
            painter.setPen(pen)
            draw_line(l_bar, interaction)
            painter.restore()
            textrect.adjust(0, 0, 0, -textoffset)

        opt.text = text
        self.drawViewItemText(style, painter, opt, textrect)


class FilterProxy(QSortFilterProxyModel):
    scorer = None

    def sort(self, *args, **kwargs):
        self.sourceModel().sort(*args, **kwargs)


class OWInteractions(OWWidget, ConcurrentWidgetMixin):
    name = __("name")
    description = __("desc")
    icon = "icons/Interactions.svg"

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        features = Output("Features", AttributeList)

    settingsHandler = DomainContextHandler()
    selection = ContextSetting([])
    feature: Variable
    feature = ContextSetting(None)
    heuristic_mode: int
    heuristic_mode = Setting(0)

    want_main_area = False
    want_control_area = True

    class Information(OWWidget.Information):
        removed_cons_feat = Msg(__("removed_cons_feat"))

    class Warning(OWWidget.Warning):
        not_enough_vars = Msg(__("not_enough_vars"))
        not_enough_inst = Msg(__("not_enough_inst"))
        no_class_var = Msg(__("no_class_var"))

    def __init__(self):
        OWWidget.__init__(self)
        ConcurrentWidgetMixin.__init__(self)

        self.keep_running = True
        self.saved_state = None
        self.progress = 0

        self.original_domain: Domain = ...
        self.data: Table = ...
        self.n_attrs = 0

        self.scorer = None
        self.heuristic = None
        self.feature_index = None

        gui.comboBox(self.controlArea, self, "heuristic_mode",
                     items=Heuristic.mode.values(),
                     callback=self.on_heuristic_combo_changed,)

        self.feature_model = DomainModel(order=DomainModel.ATTRIBUTES,
                                         separators=False,
                                         placeholder=__("all_combinations"))
        gui.comboBox(self.controlArea, self, "feature",
                     callback=self.on_feature_combo_changed,
                     model=self.feature_model, searchable=True)

        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Filter ...")
        self.filter.textChanged.connect(self.on_filter_changed)
        self.controlArea.layout().addWidget(self.filter)

        self.model = RankModel()
        self.model.setHorizontalHeaderLabels([__("interaction"), __("information_gain"),
                                              __("feature_1"), __("feature_2")])
        self.proxy = FilterProxy(filterCaseSensitivity=Qt.CaseInsensitive)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(-1)
        self.rank_table = view = QTableView(selectionBehavior=QTableView.SelectRows,
                                            selectionMode=QTableView.SingleSelection,
                                            showGrid=False,
                                            editTriggers=gui.TableView.NoEditTriggers)
        view.setSortingEnabled(True)
        view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        view.setItemDelegate(InteractionItemDelegate())
        view.setModel(self.proxy)
        view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.controlArea.layout().addWidget(view)

        self.button = gui.button(self.controlArea, self, __("start"), callback=self.toggle)
        self.button.setEnabled(False)

    @Inputs.data
    def set_data(self, data):
        self.closeContext()
        self.clear_messages()
        self.selection = {}
        self.original_domain = data and data.domain
        self.data = None
        self.n_attrs = 0
        if data is not None:
            if len(data) < 2:
                self.Warning.not_enough_inst()
            elif data.Y.size == 0:
                self.Warning.no_class_var()
            else:
                remover = Remove(Remove.RemoveConstant)
                data = Discretize()(remover(data))
                if remover.attr_results["removed"]:
                    self.Information.removed_cons_feat()
                if len(data.domain.attributes) < 2:
                    self.Warning.not_enough_vars()
                else:
                    self.data = data
                    self.n_attrs = len(data.domain.attributes)
                    self.scorer = InteractionScorer(data)
                    self.heuristic = Heuristic(self.scorer.information_gain, self.heuristic_mode)
                    self.model.set_domain(data.domain)
                    self.proxy.scorer = self.scorer
        self.feature_model.set_domain(self.data and self.data.domain)
        self.openContext(self.data)
        self.initialize()

    def initialize(self):
        if self.task is not None:
            self.keep_running = False
            self.cancel()
        self.keep_running = True
        self.saved_state = None
        self.progress = 0
        self.progressBarFinished()
        self.model.clear()
        self.filter.setText("")
        self.button.setText("Start")
        self.button.setEnabled(self.data is not None)
        if self.data is not None:
            self.toggle()

    def commit(self):
        if self.original_domain is None:
            self.Outputs.features.send(None)
            return

        self.Outputs.features.send(AttributeList(
            [self.original_domain[attr] for attr in self.selection]))

    def toggle(self):
        self.keep_running = not self.keep_running
        if not self.keep_running:
            self.button.setText("Pause")
            self.button.repaint()
            self.filter.setEnabled(False)
            self.progressBarInit()
            self.start(run, self.compute_score, self.row_for_state,
                       self.iterate_states, self.saved_state,
                       self.progress, self.state_count())
        else:
            self.button.setText("Continue")
            self.button.repaint()
            self.filter.setEnabled(True)
            self.cancel()
            self._stopped()

    def _stopped(self):
        self.progressBarFinished()
        self._select_default()

    def _select_default(self):
        n_rows = self.model.rowCount()
        if not n_rows:
            return

        if self.selection:
            for i in range(n_rows):
                names = {self.model.data(self.model.index(i, 2)),
                         self.model.data(self.model.index(i, 3))}
                if names == self.selection:
                    self.rank_table.selectRow(i)
                    break

        if not self.rank_table.selectedIndexes():
            self.rank_table.selectRow(0)

    def on_selection_changed(self, selected):
        self.selection = {self.model.data(ind) for ind in selected.indexes()[-2:]}
        self.commit()

    def on_filter_changed(self, text):
        self.proxy.setFilterFixedString(text)

    def on_feature_combo_changed(self):
        self.feature_index = self.feature and self.data.domain.index(self.feature)
        self.initialize()

    def on_heuristic_combo_changed(self):
        if self.data is not None:
            self.heuristic = Heuristic(self.scorer.information_gain, self.heuristic_mode)
        self.initialize()

    def compute_score(self, state):
        attr1, attr2 = state
        scores = (self.scorer(attr1, attr2),
                  self.scorer.information_gain[attr1],
                  self.scorer.information_gain[attr2])
        return tuple(self.scorer.normalize(score) for score in scores)

    @staticmethod
    def row_for_state(score, state):
        return [score[0], sum(score)] + list(state)

    def iterate_states(self, initial_state):
        if self.feature is not None:
            return self._iterate_by_feature(initial_state)
        if self.n_attrs > 3 and self.heuristic is not None:
            return self.heuristic.get_states(initial_state)
        return self._iterate_all(initial_state)

    def _iterate_all(self, initial_state):
        i0, j0 = initial_state or (0, 0)
        for i in range(i0, self.n_attrs):
            for j in range(j0, i):
                yield i, j
            j0 = 0

    def _iterate_by_feature(self, initial_state):
        _, j0 = initial_state or (0, 0)
        for j in range(j0, self.n_attrs):
            if j != self.feature_index:
                yield self.feature_index, j

    def state_count(self):
        if self.feature_index is None:
            return self.n_attrs * (self.n_attrs - 1) // 2
        return self.n_attrs - 1

    def on_partial_result(self, result):
        add_to_model, latest_state = result
        if add_to_model:
            self.saved_state = latest_state
            self.model.extend(add_to_model)
            self.progress = len(self.model)
            self.progressBarSet(self.progress * 100 // self.state_count())

    def on_done(self, result):
        self.button.setText(__("finished"))
        self.button.setEnabled(False)
        self.filter.setEnabled(True)
        self.keep_running = False
        self.saved_state = None
        self._stopped()

    def send_report(self):
        self.report_table(__("interactions"), self.rank_table)


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWInteractions).run(Table("iris"))
