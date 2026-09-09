# -*- coding: utf-8 -*-
"""
claude_settings_window__ui__.py
---------------------------------
Einstellungsdialog für Anthropic Claude. Der API-Key wird ausschließlich
über ``ChatBot.set_secret("claude", ...)`` in ``claude.env`` geschrieben -
NIE in ``chatbot.cfg`` und nie im Klartext-Log ausgegeben.
"""

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout,
)

PROVIDER = "claude"
DEFAULT_MODEL = "claude-sonnet-4-6"


class ClaudeSettingsWindow(QDialog):
    def __init__(self, chat_bot, parent=None):
        super().__init__(parent)
        self.bot = chat_bot
        self.setModal(True)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setText(self.bot.get_secret(PROVIDER) or "")
        self.api_key_label = QLabel()
        form.addRow(self.api_key_label, self.api_key_edit)

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
        self.setWindowTitle(tr("settings.title", provider="Claude"))
        self.api_key_label.setText(tr("settings.api_key"))
        self.api_key_edit.setPlaceholderText(tr("settings.api_key.placeholder"))
        self.model_label.setText(tr("settings.model"))
        self.saved_hint.setText(tr("settings.saved"))
        self.test_btn.setText(tr("settings.test_connection"))
        self.save_btn.setText(tr("settings.save"))
        self.cancel_btn.setText(tr("settings.cancel"))

    def _save(self) -> None:
        self.bot.set_secret(PROVIDER, self.api_key_edit.text().strip())
        self.bot.set_model(PROVIDER, self.model_edit.text().strip() or DEFAULT_MODEL)
        self.accept()

    def _test_connection(self) -> None:
        api_key = self.api_key_edit.text().strip()
        if not api_key:
            QMessageBox.warning(self, self.windowTitle(), self.bot.tr("status.no_api_key", provider="Claude"))
            return
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            client.messages.create(
                model=self.model_edit.text().strip() or DEFAULT_MODEL,
                max_tokens=8,
                messages=[{"role": "user", "content": "ping"}],
            )
            QMessageBox.information(self, self.windowTitle(), self.bot.tr("status.connected", provider="Claude"))
        except Exception as exc:
            QMessageBox.critical(self, self.windowTitle(), self.bot.tr("status.error", error=str(exc)))
