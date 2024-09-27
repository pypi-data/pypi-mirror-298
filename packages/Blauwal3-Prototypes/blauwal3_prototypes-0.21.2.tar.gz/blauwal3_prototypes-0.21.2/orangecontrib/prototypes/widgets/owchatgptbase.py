from typing import Optional

from AnyQt.QtCore import Signal, Qt
from AnyQt.QtGui import QFocusEvent
from AnyQt.QtWidgets import QLineEdit, QTextEdit

import openai
import tiktoken

from Orange.data import Table, StringVariable
from Orange.widgets import gui
from Orange.widgets.credentials import CredentialManager
from Orange.widgets.utils.concurrents import ConcurrentWidgetMixin
from Orange.widgets.utils.itemmodels import DomainModel
from Orange.widgets.settings import Setting, DomainContextHandler, \
    ContextSetting
from Orange.widgets.widget import OWWidget, Input, Msg
from orangecontrib.prototypes.i18n_config import *


def __(key):
    return i18n.t('prototypes.owchatgpt.' + key)

MODELS = ["gpt-3.5-turbo", "gpt-4", "Custom"]


def run_gpt(
        base_url: str,
        api_key: str,
        model: str,
        text: str,
        prompt_start: str,
        prompt_end: str
) -> str:
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    if model in ["gpt-3.5-turbo", "gpt-4"]:
        enc = tiktoken.encoding_for_model(model)
    else:
        enc = tiktoken.get_encoding("o200k_base")  # Use a default encoding for custom models

    text = enc.decode(enc.encode(text)[:3500])
    content = f"{prompt_start}\n{text}.\n{prompt_end}"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content},
        ],
        temperature=0
    )
    return response.choices[0].message.content


class TextEdit(QTextEdit):
    sigEditFinished = Signal()

    def focusOutEvent(self, ev: QFocusEvent):
        self.sigEditFinished.emit()
        super().focusOutEvent(ev)


class OWChatGPTBase(OWWidget, ConcurrentWidgetMixin, openclass=True):
    settingsHandler = DomainContextHandler()
    access_key = ""
    base_url = ""  # Add base_url setting
    model_index = Setting(0)
    text_var = ContextSetting(None)
    prompt_start = Setting("")
    prompt_end = Setting("")
    auto_apply = Setting(False)
    custom_model_name = Setting("")  # Add custom model name setting

    class Inputs:
        data = Input("Data", Table)

    class Warning(OWWidget.Warning):
        missing_key = Msg(__("missing_key"))
        missing_str_var = Msg(__("missing_str_var"))

    class Error(OWWidget.Error):
        unknown_error = Msg(__("unknown_error"))

    def __init__(self):
        OWWidget.__init__(self)
        ConcurrentWidgetMixin.__init__(self)
        self._data: Optional[Table] = None
        self.__text_var_model = DomainModel(valid_types=(StringVariable,))
        self.__start_text_edit: QTextEdit = None
        self.__end_text_edit: QTextEdit = None

        self.__cm = CredentialManager("Ask")
        self.access_key = self.__cm.access_key or ""

        self.setup_gui()

    def setup_gui(self):
        box = gui.vBox(self.controlArea, __("model"))
        
        # Add Base URL input
        base_url_edit: QLineEdit = gui.lineEdit(box, self, "base_url", "Base URL:",
                                                orientation=Qt.Horizontal,
                                                callback=self.__on_base_url_changed)
        
        edit: QLineEdit = gui.lineEdit(box, self, "access_key", "API Key:",
                                       orientation=Qt.Horizontal,
                                       callback=self.__on_access_key_changed)
        edit.setEchoMode(QLineEdit.Password)
        gui.comboBox(box, self, "model_index", label="Model:",
                     orientation=Qt.Horizontal,
                     items=MODELS, callback=self.__on_model_changed)

        # Add custom model name input
        self.custom_model_edit = gui.lineEdit(box, self, "custom_model_name", __("custom_model_name_label"),
                                              orientation=Qt.Horizontal,
                                              callback=self.__on_custom_model_name_changed)
        self.custom_model_edit.setEnabled(False)  # Initially disabled

        gui.comboBox(self.controlArea, self, "text_var", __("data"),
                     __("text_variable_label"), model=self.__text_var_model,
                     orientation=Qt.Horizontal, callback=self.commit.deferred)

        box = gui.vBox(self.controlArea, __("prompt"))
        gui.label(box, self, __("start_label"))
        self.__start_text_edit = TextEdit(tabChangesFocus=True)
        self.__start_text_edit.setText(self.prompt_start)
        self.__start_text_edit.sigEditFinished.connect(
            self.__on_start_text_edit_changed)
        box.layout().addWidget(self.__start_text_edit)
        gui.label(box, self, __("end_label"))
        self.__end_text_edit = TextEdit(tabChangesFocus=True)
        self.__end_text_edit.setText(self.prompt_end)
        self.__end_text_edit.sigEditFinished.connect(
            self.__on_end_text_edit_changed)
        box.layout().addWidget(self.__end_text_edit)

        gui.rubber(self.controlArea)

        gui.auto_apply(self.buttonsArea, self, "auto_apply")

    def __on_access_key_changed(self):
        self.__cm.access_key = self.access_key
        self.commit.deferred()

    def __on_start_text_edit_changed(self):
        prompt_start = self.__start_text_edit.toPlainText()
        if self.prompt_start != prompt_start:
            self.prompt_start = prompt_start
            self.commit.deferred()

    def __on_end_text_edit_changed(self):
        prompt_end = self.__end_text_edit.toPlainText()
        if self.prompt_end != prompt_end:
            self.prompt_end = prompt_end
            self.commit.deferred()

    def __on_base_url_changed(self):
        self.commit.deferred()

    def __on_model_changed(self):
        self.commit.deferred()
        # Enable custom model name input if "Custom" is selected
        self.custom_model_edit.setEnabled(self.model_index == 2)

    def __on_custom_model_name_changed(self):
        self.commit.deferred()

    @Inputs.data
    def set_data(self, data: Table):
        self.closeContext()
        self.clear_messages()
        self._data = data
        self.__text_var_model.set_domain(data.domain if data else None)
        self.text_var = self.__text_var_model[0] if self.__text_var_model \
            else None
        if data and not self.__text_var_model:
            self.Warning.missing_str_var()
        self.openContext(data)

    @gui.deferred
    def commit(self):
        self.Error.unknown_error.clear()
        self.Warning.missing_key.clear()
        if self.access_key == "":
            self.Warning.missing_key()
        self.start(self.ask_gpt)

    def ask_gpt(self):
        model = MODELS[self.model_index]
        if model == "Custom":
            model = self.custom_model_name  # Ensure custom model name is used
        result = run_gpt(self.base_url, self.access_key, model, self.text_var, self.prompt_start, self.prompt_end)
        # ... handle result ...

    def on_exception(self, ex: Exception):
        self.Error.unknown_error(ex)

    def on_partial_result(self, _):
        pass

    def onDeleteWidget(self):
        self.shutdown()
        super().onDeleteWidget()

if __name__ == "__main__":
    api_key = "sk-c44ca0e1964a4e78b5bc15ad61174edf"
    base_url = "https://api.deepseek.com"
    try:
        result = run_gpt(base_url=base_url, api_key=api_key, model="deepseek-chat", text="Hello, how are you?", prompt_start="Start:", prompt_end="End:")
        print(result)
    except Exception as e:
        print(f"Error occurred: {str(e)}")