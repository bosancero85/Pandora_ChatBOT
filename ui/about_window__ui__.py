# -*- coding: utf-8 -*-
"""
about_window__ui__.py
Über-Dialog des Pandora® ChatBot.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class AboutWindow(QDialog):
    def __init__(self, chat_bot, parent=None):
        super().__init__(parent)
        self.bot = chat_bot
        self.setModal(True)

        layout = QVBoxLayout(self)
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.title_label.font()
        font.setPointSize(font.pointSize() + 4)
        font.setBold(True)
        self.title_label.setFont(font)
        layout.addWidget(self.title_label)

        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description_label)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self.close_btn = QPushButton()
        self.close_btn.clicked.connect(self.accept)
        buttons.addWidget(self.close_btn)
        buttons.addStretch(1)
        layout.addLayout(buttons)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        tr = self.bot.tr
        self.setWindowTitle(tr("about.title"))
        self.title_label.setText(tr("app.title"))
        self.description_label.setText(tr("about.description"))
        self.close_btn.setText(tr("about.close"))
