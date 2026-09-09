# -*- coding: utf-8 -*-
"""
main_window__ui__.py
----------------------
Hauptfenster des Pandora® ChatBot. Verbindet Sidebar (Anbieter, Rollen,
Sprache, Verlauf) und ChatWidget (Nachrichten) mit dem ``ChatBot``-Objekt
und startet je nach gewähltem Anbieter den passenden Worker
(``ClaudeWorker`` / ``GeminiWorker`` / ``OllamaWorker``).
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QActionGroup
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QSplitter, QWidget,
)

from app.chat_bot import ChatBot
from app.theme_manager import DARK, LIGHT, apply_theme
from core.claude_worker import ClaudeWorker
from core.gemini_worker import GeminiWorker
from core.ollama_worker import OllamaWorker
from media_worker.ai_file_response_worker import build_file_context
from media_worker.ai_picture_response_worker import describe_image_for_context
from media_worker.ai_video_response_worker import describe_video_for_context
from ui.about_window__ui__ import AboutWindow
from ui.chat_appearance_window__ui__ import ChatAppearanceWindow
from ui.claude_settings_window__ui__ import ClaudeSettingsWindow
from ui.components.sidebar__ui__ import SidebarWidget
from ui.chat_widget__ui__ import ChatWidget
from ui.disclaimer_window__ui__ import DisclaimerWindow
from ui.gemini_settings_window__ui__ import GeminiSettingsWindow
from ui.help_window__ui__ import HelpWindow
from ui.license_window__ui__ import LicenseWindow
from ui.ollama_settings_window__ui__ import OllamaSettingsWindow


class MainWindow(QMainWindow):
    def __init__(self, chat_bot: ChatBot = None, parent=None):
        super().__init__(parent)
        self.bot = chat_bot or ChatBot()
        self._worker = None

        self.resize(
            self.bot.config.get_int("window", "width", 1280),
            self.bot.config.get_int("window", "height", 800),
        )

        self.sidebar = SidebarWidget(self.bot)
        self.chat_widget = ChatWidget(self.bot)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.chat_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([280, 1000])
        self.setCentralWidget(splitter)

        self._build_menu()
        self._connect_signals()

        # -- Darstellung wiederherstellen (Theme, Seitenleiste, Chat-Schrift)
        app = QApplication.instance()
        if app is not None:
            normalized = apply_theme(app, self.bot.theme)
            self.bot.set_theme(normalized)
            (self.theme_dark_action if normalized == DARK else self.theme_light_action).setChecked(True)

        self.sidebar.setVisible(self.bot.sidebar_visible)
        self.toggle_sidebar_action.setChecked(self.bot.sidebar_visible)

        self.sidebar.set_active_provider(self.bot.active_provider)
        self.sidebar.reload_sessions()
        if self.bot.list_sessions():
            self.bot.load_session(self.bot.list_sessions()[0]["id"])
            self.chat_widget.load_history(self.bot.history_as_messages())
        else:
            self.bot.start_new_session()

        self.retranslate_ui()

    # ------------------------------------------------------------------
    # Menü
    # ------------------------------------------------------------------
    def _build_menu(self) -> None:
        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu("")
        self.new_chat_action = self.file_menu.addAction("")
        self.new_chat_action.triggered.connect(lambda: self._on_new_session_requested())
        self.exit_action = self.file_menu.addAction("")
        self.exit_action.triggered.connect(self.close)

        self.settings_menu = menu_bar.addMenu("")
        self.claude_settings_action = self.settings_menu.addAction("")
        self.claude_settings_action.triggered.connect(lambda: self._open_settings("claude"))
        self.gemini_settings_action = self.settings_menu.addAction("")
        self.gemini_settings_action.triggered.connect(lambda: self._open_settings("gemini"))
        self.ollama_settings_action = self.settings_menu.addAction("")
        self.ollama_settings_action.triggered.connect(lambda: self._open_settings("ollama"))

        self.view_menu = menu_bar.addMenu("")

        self.toggle_sidebar_action = self.view_menu.addAction("")
        self.toggle_sidebar_action.setCheckable(True)
        self.toggle_sidebar_action.toggled.connect(self._on_toggle_sidebar)

        self.view_menu.addSeparator()

        self.theme_menu = self.view_menu.addMenu("")
        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.setExclusive(True)
        self.theme_light_action = self.theme_menu.addAction("")
        self.theme_light_action.setCheckable(True)
        self.theme_light_action.triggered.connect(lambda: self._set_theme(LIGHT))
        self.theme_dark_action = self.theme_menu.addAction("")
        self.theme_dark_action.setCheckable(True)
        self.theme_dark_action.triggered.connect(lambda: self._set_theme(DARK))
        self.theme_action_group.addAction(self.theme_light_action)
        self.theme_action_group.addAction(self.theme_dark_action)

        self.view_menu.addSeparator()

        self.chat_appearance_action = self.view_menu.addAction("")
        self.chat_appearance_action.triggered.connect(self._open_chat_appearance)

        self.help_menu = menu_bar.addMenu("")
        self.help_action = self.help_menu.addAction("")
        self.help_action.triggered.connect(self._open_help)
        self.help_menu.addSeparator()
        self.disclaimer_action = self.help_menu.addAction("")
        self.disclaimer_action.triggered.connect(self._open_disclaimer)
        self.license_action = self.help_menu.addAction("")
        self.license_action.triggered.connect(self._open_license)
        self.help_menu.addSeparator()
        self.about_action = self.help_menu.addAction("")
        self.about_action.triggered.connect(self._open_about)

    def retranslate_ui(self) -> None:
        tr = self.bot.tr
        self.setWindowTitle(tr("app.title"))
        self.file_menu.setTitle(tr("menu.file"))
        self.new_chat_action.setText(tr("menu.file.new_chat"))
        self.exit_action.setText(tr("menu.file.exit"))
        self.settings_menu.setTitle(tr("menu.settings"))
        self.claude_settings_action.setText(tr("menu.settings.claude"))
        self.gemini_settings_action.setText(tr("menu.settings.gemini"))
        self.ollama_settings_action.setText(tr("menu.settings.ollama"))
        self.view_menu.setTitle(tr("menu.view"))
        self.toggle_sidebar_action.setText(tr("menu.view.sidebar"))
        self.theme_menu.setTitle(tr("menu.view.theme"))
        self.theme_light_action.setText(tr("menu.view.theme.light"))
        self.theme_dark_action.setText(tr("menu.view.theme.dark"))
        self.chat_appearance_action.setText(tr("menu.view.chat_appearance"))
        self.help_menu.setTitle(tr("menu.help"))
        self.help_action.setText(tr("menu.help.help"))
        self.disclaimer_action.setText(tr("menu.help.disclaimer"))
        self.license_action.setText(tr("menu.help.license"))
        self.about_action.setText(tr("menu.help.about"))
        self.sidebar.retranslate_ui()
        self.chat_widget.retranslate_ui()

    # ------------------------------------------------------------------
    # Verdrahtung
    # ------------------------------------------------------------------
    def _connect_signals(self) -> None:
        self.sidebar.provider_changed.connect(self._on_provider_changed)
        self.sidebar.roles_changed.connect(self._on_roles_changed)
        self.sidebar.language_selected.connect(self._on_language_selected)
        self.sidebar.new_session_requested.connect(self._on_new_session_requested)
        self.sidebar.session_selected.connect(self._on_session_selected)
        self.sidebar.session_rename_requested.connect(self._on_session_rename_requested)
        self.sidebar.session_delete_requested.connect(self._on_session_delete_requested)

        self.chat_widget.message_sent.connect(self._on_message_sent)
        self.chat_widget.stop_requested.connect(self._on_stop_requested)
        self.chat_widget.file_attached.connect(self._on_file_attached)
        self.chat_widget.image_attached.connect(self._on_image_attached)
        self.chat_widget.video_attached.connect(self._on_video_attached)

    def _on_provider_changed(self, provider: str) -> None:
        self.bot.set_active_provider(provider)

    def _on_roles_changed(self, role_ids) -> None:
        self.bot.set_selected_roles(role_ids)

    def _on_language_selected(self, code: str) -> None:
        if self.bot.set_language(code):
            self.retranslate_ui()

    def _on_new_session_requested(self) -> None:
        self.bot.start_new_session()
        self.chat_widget.clear_messages()
        self.sidebar.reload_sessions()

    def _on_session_selected(self, session_id: str) -> None:
        data = self.bot.load_session(session_id)
        if data is not None:
            self.chat_widget.load_history(self.bot.history_as_messages())
            self.sidebar.set_active_provider(self.bot.active_provider)

    def _on_session_rename_requested(self, session_id: str) -> None:
        from PyQt6.QtWidgets import QInputDialog
        title, ok = QInputDialog.getText(self, self.bot.tr("sidebar.sessions.rename"), "")
        if ok and title.strip():
            self.bot.memory.rename_session(session_id, title.strip())
            self.sidebar.reload_sessions()

    def _on_session_delete_requested(self, session_id: str) -> None:
        self.bot.memory.delete_session(session_id)
        if self.bot.current_session_id == session_id:
            self.bot.current_session_id = None
            self.bot.start_new_session()
            self.chat_widget.clear_messages()
        self.sidebar.reload_sessions()

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------
    def _on_message_sent(self, text: str) -> None:
        self.chat_widget.add_message("user", text)
        self.bot.record_message("user", text)

        provider = self.bot.active_provider
        api_key_or_host = self.bot.get_secret(provider)
        if provider != "ollama" and not api_key_or_host:
            QMessageBox.warning(self, self.windowTitle(), self.bot.tr("status.no_api_key", provider=provider))
            return

        system_prompt = self.bot.build_system_prompt()
        history = self.bot.history_as_messages()

        if provider == "claude":
            worker = ClaudeWorker(api_key_or_host, history, system_prompt=system_prompt,
                                   model=self.bot.get_model("claude"))
        elif provider == "gemini":
            worker = GeminiWorker(api_key_or_host, history, system_prompt=system_prompt,
                                   model=self.bot.get_model("gemini"))
        else:
            worker = OllamaWorker(api_key_or_host, history, system_prompt=system_prompt,
                                   model=self.bot.get_model("ollama"))

        worker.chunk_received.connect(self.chat_widget.append_stream_chunk)
        worker.finished_response.connect(self._on_response_finished)
        worker.error_occurred.connect(self._on_response_error)
        self._worker = worker

        self.chat_widget.set_busy(True)
        worker.start()

    def _on_stop_requested(self) -> None:
        if self._worker is not None:
            self._worker.stop()

    def _on_response_finished(self, full_text: str) -> None:
        self.bot.record_message("assistant", full_text)
        self.chat_widget.end_streaming_response()
        self.chat_widget.set_busy(False)
        self._worker = None
        self.sidebar.reload_sessions()

    def _on_response_error(self, message: str) -> None:
        self.chat_widget.end_streaming_response()
        self.chat_widget.set_busy(False)
        self._worker = None
        QMessageBox.critical(self, self.windowTitle(), self.bot.tr("status.error", error=message))

    # ------------------------------------------------------------------
    # Anhänge
    # ------------------------------------------------------------------
    def _append_to_input(self, text: str) -> None:
        current = self.chat_widget.input_edit.toPlainText()
        combined = f"{current}\n{text}" if current.strip() else text
        self.chat_widget.input_edit.setPlainText(combined)

    def _on_file_attached(self, path: str) -> None:
        self._append_to_input(build_file_context(path))

    def _on_image_attached(self, path: str) -> None:
        # Anthropic/Claude kann Bilder direkt verarbeiten (siehe
        # media_worker/ai_picture_response_worker.build_image_content_block);
        # im einfachen Textverlauf hier wird der Anhang zunächst nur
        # angekündigt, damit die Sitzung als reiner Text persistiert bleibt.
        self._append_to_input(describe_image_for_context(path))

    def _on_video_attached(self, path: str) -> None:
        self._append_to_input(describe_video_for_context(path))

    # ------------------------------------------------------------------
    # Dialoge
    # ------------------------------------------------------------------
    def _open_settings(self, provider: str) -> None:
        dialogs = {
            "claude": ClaudeSettingsWindow,
            "gemini": GeminiSettingsWindow,
            "ollama": OllamaSettingsWindow,
        }
        dialog = dialogs[provider](self.bot, self)
        dialog.exec()

    def _open_about(self) -> None:
        AboutWindow(self.bot, self).exec()

    def _open_help(self) -> None:
        HelpWindow(self.bot, self).exec()

    def _open_disclaimer(self) -> None:
        DisclaimerWindow(self.bot, self).exec()

    def _open_license(self) -> None:
        LicenseWindow(self.bot, self).exec()

    def _open_chat_appearance(self) -> None:
        dialog = ChatAppearanceWindow(self.bot, self)
        if dialog.exec():
            self.chat_widget.apply_appearance(dialog.result_appearance())

    # ------------------------------------------------------------------
    # Ansicht (Theme, Seitenleiste)
    # ------------------------------------------------------------------
    def _on_toggle_sidebar(self, visible: bool) -> None:
        self.sidebar.setVisible(visible)
        self.bot.set_sidebar_visible(visible)

    def _set_theme(self, theme: str) -> None:
        app = QApplication.instance()
        if app is None:
            return
        normalized = apply_theme(app, theme)
        self.bot.set_theme(normalized)
        action = self.theme_dark_action if normalized == DARK else self.theme_light_action
        if not action.isChecked():
            action.setChecked(True)

    def closeEvent(self, event) -> None:
        self.bot.config.set("window", "width", self.width(), save=False)
        self.bot.config.set("window", "height", self.height(), save=True)
        super().closeEvent(event)
