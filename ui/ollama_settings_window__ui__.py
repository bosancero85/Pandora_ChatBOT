# -*- coding: utf-8 -*-
"""
ollama_settings_window__ui__.py
---------------------------------
Einstellungsdialog für Ollama. Ollama benötigt normalerweise keinen
API-Key, sondern nur die Server-Adresse - diese wird trotzdem bewusst in
``ollama.env`` abgelegt (nicht in ``chatbot.cfg``), damit alle
anbieterspezifischen Verbindungsdaten konsistent an einer Stelle liegen.
"""

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout,
)

PROVIDER = "ollama"
DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1"


class OllamaSettingsWindow(QDialog):
    def __init__(self, chat_bot, parent=None):
        super().__init__(parent)
        self.bot = chat_bot
        self.setModal(True)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.host_edit = QLineEdit()
        self.host_edit.setText(self.bot.get_secret(PROVIDER) or DEFAULT_HOST)
        self.host_label = QLabel()
        form.addRow(self.host_label, self.host_edit)

        self.model_edit = QLineEdit()
        self.model_edit.setText(self.bot.get_model(PROVIDER) or DEFAULT_MODEL)
        self.model_label = QLabel()
        form.addRow(self.model_label, self.model_edit)

        layout.addLayout(form)

        self.saved_hint = QLabel()
        self.saved_hint.setWordWrap(True)
        layout.addWidget(self.saved_hint)

        buttons = QHBoxLayout()
        self.test_btn = QPushButton()
        self.test_btn.clicked.connect(self._test_connection)
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self._save)
        self.cancel_btn = QPushButton()
        self.cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(self.test_btn)
        buttons.addStretch(1)
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addLayout(buttons)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        tr = self.bot.tr
        self.setWindowTitle(tr("settings.title", provider="Ollama"))
        self.host_label.setText(tr("settings.host"))
        self.model_label.setText(tr("settings.model"))
        self.saved_hint.setText(tr("settings.saved"))
        self.test_btn.setText(tr("settings.test_connection"))
        self.save_btn.setText(tr("settings.save"))
        self.cancel_btn.setText(tr("settings.cancel"))

    def _save(self) -> None:
        self.bot.set_secret(PROVIDER, self.host_edit.text().strip() or DEFAULT_HOST)
        self.bot.set_model(PROVIDER, self.model_edit.text().strip() or DEFAULT_MODEL)
        self.accept()

    def _test_connection(self) -> None:
        host = self.host_edit.text().strip() or DEFAULT_HOST
        try:
            import ollama
            client = ollama.Client(host=host)
            client.list()
            QMessageBox.information(self, self.windowTitle(), self.bot.tr("status.connected", provider="Ollama"))
        except Exception as exc:
            QMessageBox.critical(self, self.windowTitle(), self.bot.tr("status.error", error=str(exc)))
