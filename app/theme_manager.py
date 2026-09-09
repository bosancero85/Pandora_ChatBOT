# -*- coding: utf-8 -*-
"""
theme_manager.py
------------------
Stellt das helle und dunkle Pandora®-Farbschema (Qt-Stylesheets) bereit
und wendet es zentral auf die ``QApplication`` an. Der aktuell gewählte
Modus wird über ``ConfigManager`` (``general.theme``) persistiert, damit
er beim nächsten Start erhalten bleibt.
"""

from typing import Optional

LIGHT = "light"
DARK = "dark"

_DARK_QSS = """
QWidget {
    background-color: #14141c;
    color: #e6e6f0;
    selection-background-color: #00d9ff;
    selection-color: #0a0a12;
}
QMainWindow, QDialog {
    background-color: #14141c;
}
QMenuBar {
    background-color: #1b1b26;
    color: #e6e6f0;
}
QMenuBar::item:selected {
    background-color: #2a2a3a;
}
QMenu {
    background-color: #1b1b26;
    color: #e6e6f0;
    border: 1px solid #2a2a3a;
}
QMenu::item:selected {
    background-color: #00d9ff;
    color: #0a0a12;
}
QGroupBox {
    border: 1px solid #2a2a3a;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 8px;
    color: #9fe8ff;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QListWidget {
    background-color: #1e1e2a;
    color: #e6e6f0;
    border: 1px solid #33334a;
    border-radius: 4px;
    padding: 4px;
}
QPushButton {
    background-color: #22222f;
    color: #e6e6f0;
    border: 1px solid #3a3a52;
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: #2c2c40;
    border-color: #00d9ff;
}
QPushButton:pressed {
    background-color: #00d9ff;
    color: #0a0a12;
}
QPushButton:disabled {
    color: #666677;
    border-color: #2a2a3a;
}
QScrollArea {
    border: none;
}
QScrollBar:vertical {
    background: #1b1b26;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #3a3a52;
    border-radius: 5px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #00d9ff;
}
#BubbleUser {
    background-color: #12384a;
    border-radius: 10px;
}
#BubbleAssistant {
    background-color: #201e2c;
    border-radius: 10px;
}
#BubbleAuthor {
    color: #00d9ff;
    font-weight: bold;
}
"""

_LIGHT_QSS = """
QWidget {
    background-color: #f5f6fa;
    color: #1b1b26;
    selection-background-color: #0078a8;
    selection-color: #ffffff;
}
QMainWindow, QDialog {
    background-color: #f5f6fa;
}
QMenuBar {
    background-color: #ffffff;
    color: #1b1b26;
}
QMenuBar::item:selected {
    background-color: #e1e6ef;
}
QMenu {
    background-color: #ffffff;
    color: #1b1b26;
    border: 1px solid #d3d7e0;
}
QMenu::item:selected {
    background-color: #0078a8;
    color: #ffffff;
}
QGroupBox {
    border: 1px solid #d3d7e0;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 8px;
    color: #0078a8;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QListWidget {
    background-color: #ffffff;
    color: #1b1b26;
    border: 1px solid #c7cbd6;
    border-radius: 4px;
    padding: 4px;
}
QPushButton {
    background-color: #ffffff;
    color: #1b1b26;
    border: 1px solid #c7cbd6;
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: #e9edf5;
    border-color: #0078a8;
}
QPushButton:pressed {
    background-color: #0078a8;
    color: #ffffff;
}
QPushButton:disabled {
    color: #a0a4ae;
    border-color: #d3d7e0;
}
QScrollArea {
    border: none;
}
QScrollBar:vertical {
    background: #eef0f5;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #c7cbd6;
    border-radius: 5px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #0078a8;
}
#BubbleUser {
    background-color: #d9edf7;
    border-radius: 10px;
}
#BubbleAssistant {
    background-color: #ffffff;
    border-radius: 10px;
}
#BubbleAuthor {
    color: #0078a8;
    font-weight: bold;
}
"""

_STYLESHEETS = {
    LIGHT: _LIGHT_QSS,
    DARK: _DARK_QSS,
}


def normalize_theme(value: Optional[str]) -> str:
    """Wandelt beliebige gespeicherte Theme-Werte (z.B. das alte
    ``"pandora_dark"``) auf genau ``"light"`` oder ``"dark"`` ab."""
    value = (value or "").strip().lower()
    return LIGHT if "light" in value or "hell" in value else DARK


def stylesheet_for(theme: str) -> str:
    return _STYLESHEETS.get(normalize_theme(theme), _DARK_QSS)


def apply_theme(app, theme: str) -> str:
    """Wendet das Theme auf die laufende ``QApplication`` an und gibt den
    normalisierten Theme-Namen (``"light"``/``"dark"``) zurück."""
    normalized = normalize_theme(theme)
    app.setStyleSheet(stylesheet_for(normalized))
    return normalized
