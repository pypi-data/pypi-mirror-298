from AnyQt.QtWidgets import QPlainTextEdit

from Orange.data import Table
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from orangecontrib.prototypes.widgets.owchatgptbase import OWChatGPTBase, \
    run_gpt, MODELS
from orangecontrib.prototypes.i18n_config import *


def __(key):
    return i18n.t('prototypes.owchatgpt.' + key)

class OWChatGPT(OWChatGPTBase):
    name = __("name")
    description = __("desc")
    icon = "icons/chatgpt.svg"
    priority = 10
    keywords = ["text", "gpt"]

    auto_apply = Setting(True)

    def __init__(self):
        self.__answer_text_edit: QPlainTextEdit = None
        super().__init__()

    def setup_gui(self):
        super().setup_gui()
        box = gui.vBox(self.mainArea, __("answer"))
        self.__answer_text_edit = QPlainTextEdit(readOnly=True)
        box.layout().addWidget(self.__answer_text_edit)

    def set_data(self, data: Table):
        super().set_data(data)
        self.commit.now()

    def on_done(self, answer: str):
        self.__answer_text_edit.setPlainText(answer)

    def ask_gpt(self, state) -> str:
        if not self._data or not self.text_var or not self.access_key:
            return ""

        texts = self._data.get_column(self.text_var)
        text = "\n".join(texts)

        state.set_progress_value(4)
        state.set_status(__("thinking"))
        if state.is_interruption_requested():
            raise Exception

        # Use custom model name if "Custom" is selected
        model = self.custom_model_name if MODELS[self.model_index] == __("custom_model_name") else MODELS[self.model_index]
        return run_gpt(self.base_url, self.access_key, model, text, self.prompt_start, self.prompt_end)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview

    WidgetPreview(OWChatGPT).run(set_data=Table("zoo"))
