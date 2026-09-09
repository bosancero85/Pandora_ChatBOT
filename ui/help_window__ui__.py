# -*- coding: utf-8 -*-
"""
help_window__ui__.py
--------------------------
Ausführlicher Hilfe-Dialog: Tab 1 erklärt die Grundeinrichtung (Anbieter
wählen, Rollen auswählen, loslegen), Tab 2 zeigt für jeden Anbieter
(Claude/Gemini/Ollama) eine Schritt-für-Schritt-Anleitung zum Beschaffen
eines eigenen API-Keys, inkl. Button zum direkten Öffnen der jeweiligen
Anbieter-Seite. Alle Texte kommen aus den Sprachpaketen
(assets/language_packs/*/*.json), sind also automatisch mehrsprachig.
"""

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QDialog, QFrame, QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QTabWidget, QVBoxLayout, QWidget,
)

# Anbieter-Seiten zum Erstellen/Verwalten eines API-Keys. Diese URLs sind
# nicht sprachabhängig und liegen daher bewusst im Code statt in den
# Sprachpaketen.
PROVIDER_URLS = {
    "claude": "https://console.anthropic.com/settings/keys",
    "gemini": "https://aistudio.google.com/apikey",
    "ollama": "https://ollama.com/download",
}


class HelpWindow(QDialog):
    def __init__(self, chat_bot, parent=None):
        super().__init__(parent)
        self.bot = chat_bot
        self.setModal(True)
        self.resize(560, 520)

        root = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        root.addWidget(self.tabs, 1)

        self.setup_tab = self._build_setup_tab()
        self.api_keys_tab = self._build_api_keys_tab()
        self.tabs.addTab(self.setup_tab, "")
        self.tabs.addTab(self.api_keys_tab, "")

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self.close_btn = QPushButton()
        self.close_btn.clicked.connect(self.accept)
        buttons.addWidget(self.close_btn)
        root.addLayout(buttons)

        self.retranslate_ui()

    # ------------------------------------------------------------------
    # Tab 1: Einrichtung
    # ------------------------------------------------------------------
    def _build_setup_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.setup_intro_label = QLabel()
        self.setup_intro_label.setWordWrap(True)
        layout.addWidget(self.setup_intro_label)

        self.setup_step_labels = []
        for _ in range(4):
            label = QLabel()
            label.setWordWrap(True)
            label.setContentsMargins(8, 4, 0, 4)
            self.setup_step_labels.append(label)
            layout.addWidget(label)

        layout.addStretch(1)
        return widget

    # ------------------------------------------------------------------
    # Tab 2: API-Keys je Anbieter
    # ------------------------------------------------------------------
    def _build_api_keys_tab(self) -> QWidget:
        outer = QWidget()
        outer_layout = QVBoxLayout(outer)

        self.api_keys_intro_label = QLabel()
        self.api_keys_intro_label.setWordWrap(True)
        outer_layout.addWidget(self.api_keys_intro_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer_layout.addWidget(scroll, 1)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        scroll.setWidget(container)

        self.provider_groups = {}
        for provider in ("claude", "gemini", "ollama"):
            group = QGroupBox()
            group_layout = QVBoxLayout(group)

            steps_label = QLabel()
            steps_label.setWordWrap(True)
            group_layout.addWidget(steps_label)

            open_btn = QPushButton()
            open_btn.clicked.connect(
                lambda _checked=False, p=provider: QDesktopServices.openUrl(QUrl(PROVIDER_URLS[p]))
            )
            group_layout.addWidget(open_btn)

            container_layout.addWidget(group)
            self.provider_groups[provider] = {
                "group": group, "steps_label": steps_label, "open_btn": open_btn,
            }

        container_layout.addStretch(1)
        return outer

    # ------------------------------------------------------------------
    def retranslate_ui(self) -> None:
        tr = self.bot.tr
        self.setWindowTitle(tr("help.title"))
        self.tabs.setTabText(0, tr("help.tabs.setup"))
        self.tabs.setTabText(1, tr("help.tabs.api_keys"))
        self.close_btn.setText(tr("dialog.ok"))

        self.setup_intro_label.setText(tr("help.setup.intro"))
        for i, label in enumerate(self.setup_step_labels, start=1):
            label.setText(tr(f"help.setup.step{i}"))

        self.api_keys_intro_label.setText(tr("help.api_keys.intro"))
        provider_titles = {
            "claude": "Claude", "gemini": "Gemini", "ollama": "Ollama",
        }
        for provider, widgets in self.provider_groups.items():
            title = tr(f"help.api_keys.{provider}.title") or provider_titles[provider]
            widgets["group"].setTitle(title)
            widgets["steps_label"].setText(tr(f"help.api_keys.{provider}.steps"))
            widgets["open_btn"].setText(tr("help.open_page"))
