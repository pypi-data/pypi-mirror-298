from Orange.data import Table
from Orange.base import Model
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.widgets.utils.concurrents import TaskState, ConcurrentWidgetMixin
from Orange.widgets.widget import Msg
from Orange.widgets import gui
from Orange.widgets.settings import Setting

from AnyQt.QtCore import Qt

from orangecontrib.prototypes.modeling.scoringsheet import ScoringSheetLearner

from orangecontrib.prototypes.i18n_config import *

def __(key):
    return i18n.t('prototypes.owscoringsheet.' + key)

class ScoringSheetRunner:
    @staticmethod
    def run(learner: ScoringSheetLearner, data: Table, state: TaskState) -> Model:
        if data is None:
            return None
        state.set_status("Learning...")
        model = learner(data)
        return model


class OWScoringSheet(OWBaseLearner, ConcurrentWidgetMixin):
    name = __("name")
    description = __("desc")
    icon = "icons/ScoringSheet.svg"
    # priority = 90

    LEARNER = ScoringSheetLearner

    class Inputs(OWBaseLearner.Inputs):
        pass

    class Outputs(OWBaseLearner.Outputs):
        pass

    # Preprocessing
    num_attr_after_selection = Setting(20)

    # Scoring Sheet Settings
    num_decision_params = Setting(5)
    max_points_per_param = Setting(5)
    custom_features_checkbox = Setting(False)
    num_input_features = Setting(1)

    # Warning messages
    class Information(OWBaseLearner.Information):
        custom_number_of_input_features_used = Msg(__("custom_number_of_input_features_used"))

    def __init__(self):
        ConcurrentWidgetMixin.__init__(self)
        OWBaseLearner.__init__(self)

    def add_main_layout(self):
        box = gui.vBox(self.controlArea, __("preprocessing"))

        self.num_attr_after_selection_spin = gui.spin(
            box,
            self,
            "num_attr_after_selection",
            minv=1,
            maxv=100,
            step=1,
            label=__("number_of_attributes_after_feature_selection"),
            orientation=Qt.Horizontal,
            alignment=Qt.AlignRight,
            callback=self.settings_changed,
            controlWidth=45,
        )

        box = gui.vBox(self.controlArea, __("model_parameters"))

        gui.spin(
            box,
            self,
            "num_decision_params",
            minv=1,
            maxv=50,
            step=1,
            label=__("maximum_number_of_decision_parameters"),
            orientation=Qt.Horizontal,
            alignment=Qt.AlignRight,
            callback=self.settings_changed,
            controlWidth=45,
        ),

        gui.spin(
            box,
            self,
            "max_points_per_param",
            minv=1,
            maxv=100,
            step=1,
            label=__("maximum_points_per_decision_parameter"),
            orientation=Qt.Horizontal,
            alignment=Qt.AlignRight,
            callback=self.settings_changed,
            controlWidth=45,
        ),

        gui.checkBox(
            box,
            self,
            "custom_features_checkbox",
            label=__("custom_number_of_input_features"),
            callback=[self.settings_changed, self.custom_input_features],
        ),

        self.custom_features = gui.spin(
            box,
            self,
            "num_input_features",
            minv=1,
            maxv=50,
            step=1,
            label=__("number_of_input_features_used"),
            orientation=Qt.Horizontal,
            alignment=Qt.AlignRight,
            callback=self.settings_changed,
            controlWidth=45,
        )

        self.custom_input_features()

    def custom_input_features(self):
        """
        Enable or disable the custom input features spinbox based on the value of the custom_features_checkbox.
        Also, add or remove the Information message about the number of input features.
        """
        self.custom_features.setEnabled(self.custom_features_checkbox)
        if self.custom_features_checkbox:
            self.Information.custom_number_of_input_features_used()
        else:
            self.Information.custom_number_of_input_features_used.clear()
        self.apply()

    @Inputs.data
    def set_data(self, data):
        self.cancel()
        super().set_data(data)

    @Inputs.preprocessor
    def set_preprocessor(self, preprocessor):
        self.cancel()
        super().set_preprocessor(preprocessor)

        # Enable or disable the spin box based on whether a preprocessor is set
        self.num_attr_after_selection_spin.setEnabled(preprocessor is None)
        if preprocessor:
            self.Information.ignored_preprocessors()
        else:
            self.Information.ignored_preprocessors.clear()

    def create_learner(self):
        return self.LEARNER(
            num_attr_after_selection=self.num_attr_after_selection,
            num_decision_params=self.num_decision_params,
            max_points_per_param=self.max_points_per_param,
            num_input_features=self.num_input_features
            if self.custom_features_checkbox
            else None,
            preprocessors=self.preprocessors,
        )

    def update_model(self):
        self.cancel()
        self.show_fitting_failed(None)
        self.model = None
        if self.data is not None:
            self.start(ScoringSheetRunner.run, self.learner, self.data)
        else:
            self.Outputs.model.send(None)

    def get_learner_parameters(self):
        return (
            self.num_decision_params,
            self.max_points_per_param,
            self.num_input_features,
        )

    def on_partial_result(self, _):
        pass

    def on_done(self, result: Model):
        assert isinstance(result, Model) or result is None
        self.model = result
        self.Outputs.model.send(result)

    def on_exception(self, ex):
        self.cancel()
        self.Outputs.model.send(None)
        if isinstance(ex, BaseException):
            self.show_fitting_failed(ex)

    def onDeleteWidget(self):
        self.shutdown()
        super().onDeleteWidget()


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview

    WidgetPreview(OWScoringSheet).run()
