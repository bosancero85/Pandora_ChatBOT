# -*- coding: utf-8 -*-
"""
license_window__ui__.py
---------------------------
Lizenz-Dialog (Hilfe -> Lizenz). Text kommt vollständig aus den
Sprachpaketen (license.title / license.body), ist also automatisch
mehrsprachig.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,
)


class LicenseWindow(QDialog):
    def __init__(self, chat_bot, parent=None):
        super().__init__(parent)
        self.bot = chat_bot
        self.setModal(True)
        self.resize(520, 420)

        layout = QVBoxLayout(self)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(scroll, 1)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        self.body_label = QLabel()
        self.body_label.setWordWrap(True)
        self.body_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        container_layout.addWidget(self.body_label)
        container_layout.addStretch(1)
        scroll.setWidget(container)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self.close_btn = QPushButton()
        self.close_btn.clicked.connect(self.accept)
        buttons.addWidget(self.close_btn)
        layout.addLayout(buttons)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        tr = self.bot.tr
        self.setWindowTitle(tr("license.title"))
        self.body_label.setText(tr("license.body"))
        self.close_btn.setText(tr("dialog.ok"))
