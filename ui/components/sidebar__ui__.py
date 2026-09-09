# -*- coding: utf-8 -*-
"""
sidebar__ui__.py
-----------------
Linke Seitenleiste: KI-Anbieter, Rollen (automatisch geladen, per
Checkbox mehrfach auswählbar), Sprache und Verlauf (Sessions).

Die Rollenliste wird beim Erzeugen und über ``reload_roles()`` neu aus
``RoleManager.list_roles()`` befüllt - neue ``role_XXXXX.yar``-Dateien im
Rollen-Ordner erscheinen also ohne Codeänderung, einfach per Neuladen.
"""

from typing import List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView, QComboBox, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout,
    QWidget,
)


class SidebarWidget(QWidget):
    """Linke Seitenleiste mit Anbieter-, Rollen-, Sprach- und Verlaufsauswahl."""

    provider_changed = pyqtSignal(str)
    roles_changed = pyqtSignal(list)          # Liste der ausgewählten role_ids
    language_selected = pyqtSignal(str)       # Sprachcode, z.B. "de"
    new_session_requested = pyqtSignal()
    session_selected = pyqtSignal(str)        # session_id
    session_rename_requested = pyqtSignal(str)
    session_delete_requested = pyqtSignal(str)

    def __init__(self, chat_bot, parent=None):
        super().__init__(parent)
        self.bot = chat_bot
        self._role_items: List[QListWidgetItem] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(10)

        # -- Anbieter ---------------------------------------------------
        self.provider_label = QLabel()
        root.addWidget(self.provider_label)
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["claude", "gemini", "ollama"])
        self.provider_combo.currentTextChanged.connect(self.provider_changed.emit)
        root.addWidget(self.provider_combo)

        # -- Sprache ------------------------------------------------------
        self.language_label = QLabel()
        root.addWidget(self.language_label)
        self.language_combo = QComboBox()
        self.language_combo.currentIndexChanged.connect(self._on_language_index_changed)
        root.addWidget(self.language_combo)

        # -- Rollen (Mehrfachauswahl) ------------------------------------
        self.roles_group = QGroupBox()
        roles_layout = QVBoxLayout(self.roles_group)

        self.role_search = QLineEdit()
        roles_layout.addWidget(self.role_search)
        self.role_search.textChanged.connect(self._filter_roles)

        self.role_list = QListWidget()
        self.role_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.role_list.itemChanged.connect(self._on_role_item_changed)
        roles_layout.addWidget(self.role_list, 1)

        role_buttons = QHBoxLayout()
        self.select_all_btn = QPushButton()
        self.select_all_btn.clicked.connect(lambda: self._set_all_roles(True))
        self.select_none_btn = QPushButton()
        self.select_none_btn.clicked.connect(lambda: self._set_all_roles(False))
        role_buttons.addWidget(self.select_all_btn)
        role_buttons.addWidget(self.select_none_btn)
        roles_layout.addLayout(role_buttons)

        root.addWidget(self.roles_group, 1)

        # -- Verlauf / Sessions -------------------------------------------
        self.sessions_group = QGroupBox()
        sessions_layout = QVBoxLayout(self.sessions_group)

        self.new_session_btn = QPushButton()
        self.new_session_btn.clicked.connect(self.new_session_requested.emit)
        sessions_layout.addWidget(self.new_session_btn)

        self.session_list = QListWidget()
        self.session_list.itemActivated.connect(
            lambda item: self.session_selected.emit(item.data(Qt.ItemDataRole.UserRole))
        )
        sessions_layout.addWidget(self.session_list, 1)

        session_buttons = QHBoxLayout()
        self.rename_session_btn = QPushButton()
        self.rename_session_btn.clicked.connect(self._request_rename_current)
        self.delete_session_btn = QPushButton()
        self.delete_session_btn.clicked.connect(self._request_delete_current)
        session_buttons.addWidget(self.rename_session_btn)
        session_buttons.addWidget(self.delete_session_btn)
        sessions_layout.addLayout(session_buttons)

        root.addWidget(self.sessions_group, 1)

        self.retranslate_ui()
        self.reload_languages()
        self.reload_roles()

    # ------------------------------------------------------------------
    # Übersetzung
    # ------------------------------------------------------------------
    def retranslate_ui(self) -> None:
        tr = self.bot.tr
        self.provider_label.setText(tr("sidebar.provider"))
        self.language_label.setText(tr("sidebar.language"))
        self.roles_group.setTitle(tr("sidebar.roles"))
        self.role_search.setPlaceholderText(tr("sidebar.roles.search"))
        self.select_all_btn.setText(tr("sidebar.roles.select_all"))
        self.select_none_btn.setText(tr("sidebar.roles.select_none"))
        self.sessions_group.setTitle(tr("sidebar.sessions"))
        self.new_session_btn.setText(tr("sidebar.sessions.new"))
        self.rename_session_btn.setText(tr("sidebar.sessions.rename"))
        self.delete_session_btn.setText(tr("sidebar.sessions.delete"))
        self._relabel_roles()

    # ------------------------------------------------------------------
    # Sprache
    # ------------------------------------------------------------------
    def reload_languages(self) -> None:
        self.language_combo.blockSignals(True)
        self.language_combo.clear()
        for code, meta in sorted(self.bot.languages.available_languages().items()):
            label = f"{meta.get('flag', '')} {meta.get('name', code)}".strip()
            self.language_combo.addItem(label, code)
        idx = self.language_combo.findData(self.bot.languages.current_language)
        if idx >= 0:
            self.language_combo.setCurrentIndex(idx)
        self.language_combo.blockSignals(False)

    def _on_language_index_changed(self, index: int) -> None:
        code = self.language_combo.itemData(index)
        if code:
            self.language_selected.emit(code)

    # ------------------------------------------------------------------
    # Rollen (automatisch geladen, Mehrfachauswahl per Checkbox)
    # ------------------------------------------------------------------
    def reload_roles(self) -> None:
        """Lädt die Rollenliste neu aus dem RoleManager und markiert die
        aktuell in der Konfiguration ausgewählten Rollen wieder als
        angehakt."""
        self.bot.roles.reload()
        selected = set(self.bot.selected_role_ids)

        self.role_list.blockSignals(True)
        self.role_list.clear()
        self._role_items = []
        for role in self.bot.roles.list_roles():
            item = QListWidgetItem(self._role_label(role))
            item.setData(Qt.ItemDataRole.UserRole, role.role_id)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if role.role_id in selected else Qt.CheckState.Unchecked
            )
            self.role_list.addItem(item)
            self._role_items.append(item)
        self.role_list.blockSignals(False)

    def _role_label(self, role) -> str:
        tr = self.bot.tr
        category = tr(f"role.category.{role.category}")
        if category.startswith("role.category."):
            category = role.category
        return f"{category} · {role.display_name}"

    def _relabel_roles(self) -> None:
        for item in self._role_items:
            role_id = item.data(Qt.ItemDataRole.UserRole)
            role = self.bot.roles.get_role(role_id)
            if role is not None:
                item.setText(self._role_label(role))

    def _filter_roles(self, text: str) -> None:
        text = text.strip().lower()
        for item in self._role_items:
            item.setHidden(text not in item.text().lower())

    def _on_role_item_changed(self, _item: QListWidgetItem) -> None:
        self.roles_changed.emit(self.selected_role_ids())

    def _set_all_roles(self, checked: bool) -> None:
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        self.role_list.blockSignals(True)
        for item in self._role_items:
            if not item.isHidden():
                item.setCheckState(state)
        self.role_list.blockSignals(False)
        self.roles_changed.emit(self.selected_role_ids())

    def selected_role_ids(self) -> List[str]:
        return [
            item.data(Qt.ItemDataRole.UserRole)
            for item in self._role_items
            if item.checkState() == Qt.CheckState.Checked
        ]

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------
    def reload_sessions(self) -> None:
        self.session_list.clear()
        for session in self.bot.list_sessions():
            item = QListWidgetItem(session.get("title", "Chat"))
            item.setData(Qt.ItemDataRole.UserRole, session.get("id"))
            self.session_list.addItem(item)

    def _current_session_id(self):
        item = self.session_list.currentItem()
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def _request_rename_current(self) -> None:
        session_id = self._current_session_id()
        if session_id:
            self.session_rename_requested.emit(session_id)

    def _request_delete_current(self) -> None:
        session_id = self._current_session_id()
        if session_id:
            self.session_delete_requested.emit(session_id)

    def set_active_provider(self, provider: str) -> None:
        idx = self.provider_combo.findText(provider)
        if idx >= 0:
            self.provider_combo.blockSignals(True)
            self.provider_combo.setCurrentIndex(idx)
            self.provider_combo.blockSignals(False)
