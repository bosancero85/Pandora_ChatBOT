# -*- coding: utf-8 -*-
"""
chat_appearance_window__ui__.py
---------------------------------
Dialog zum Anpassen der Chat-Darstellung: Schriftart, Schriftgröße und
Schriftfarbe der Nachrichtentexte im Chatverlauf (``ui/chat_widget__ui__.py``
/ ``ui/components/massage_bubble__ui__.py``). Erreichbar über
Ansicht -> "Schrift & Farbe im Chat …".
"""

from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QColorDialog, QDialog, QFontComboBox, QFormLayout, QHBoxLayout, QLabel,
    QPushButton, QSpinBox, QVBoxLayout,
)


class ChatAppearanceWindow(QDialog):
    """Kleiner Einstellungsdialog für Schriftart/-größe/-farbe im Chat."""

    def __init__(self, chat_bot, parent=None):
        super().__init__(parent)
        self.bot = chat_bot
        appearance = self.bot.chat_appearance()
        self._color = appearance.get("font_color") or ""

        form = QFormLayout()

        self.font_combo = QFontComboBox()
        if appearance.get("font_family"):
            self.font_combo.setCurrentFont(QFont(appearance["font_family"]))
        self.font_label = QLabel()
        form.addRow(self.font_label, self.font_combo)

        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 32)
        self.size_spin.setValue(int(appearance.get("font_size") or 13))
        self.size_label = QLabel()
        form.addRow(self.size_label, self.size_spin)

        color_row = QHBoxLayout()
        self.color_btn = QPushButton()
        self.color_btn.clicked.connect(self._pick_color)
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(24, 24)
        color_row.addWidget(self.color_btn)
        color_row.addWidget(self.color_preview)
        color_row.addStretch(1)
        self.color_label = QLabel()
        form.addRow(self.color_label, color_row)

        self.preview_label = QLabel()
        self.preview_label.setWordWrap(True)
        self.preview_label.setMinimumHeight(40)

        button_row = QHBoxLayout()
        self.reset_btn = QPushButton()
        self.reset_btn.clicked.connect(self._reset)
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self._save)
        self.cancel_btn = QPushButton()
        self.cancel_btn.clicked.connect(self.reject)
        button_row.addWidget(self.reset_btn)
        button_row.addStretch(1)
        button_row.addWidget(self.cancel_btn)
        button_row.addWidget(self.save_btn)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addWidget(self.preview_label)
        root.addLayout(button_row)

        self.font_combo.currentFontChanged.connect(self._update_preview)
        self.size_spin.valueChanged.connect(self._update_preview)

        self.retranslate_ui()
        self._update_color_preview()
        self._update_preview()

    # ------------------------------------------------------------------
    def retranslate_ui(self) -> None:
        tr = self.bot.tr
        self.setWindowTitle(tr("chat_appearance.title"))
        self.font_label.setText(tr("chat_appearance.font_family"))
        self.size_label.setText(tr("chat_appearance.font_size"))
        self.color_label.setText(tr("chat_appearance.font_color"))
        self.color_btn.setText(tr("chat_appearance.pick_color"))
        self.reset_btn.setText(tr("chat_appearance.reset"))
        self.save_btn.setText(tr("settings.save"))
        self.cancel_btn.setText(tr("settings.cancel"))
        self._update_preview()

    # ------------------------------------------------------------------
    def _pick_color(self) -> None:
        initial = QColor(self._color) if self._color else QColor("#e6e6f0")
        color = QColorDialog.getColor(initial, self, self.bot.tr("chat_appearance.pick_color"))
        if color.isValid():
            self._color = color.name()
            self._update_color_preview()
            self._update_preview()

    def _update_color_preview(self) -> None:
        swatch = self._color or "transparent"
        border = "1px solid #888"
        self.color_preview.setStyleSheet(
            f"background-color: {swatch}; border: {border}; border-radius: 4px;"
        )

    def _reset(self) -> None:
        self._color = ""
        self.font_combo.setCurrentFont(QFont())
        self.size_spin.setValue(13)
        self._update_color_preview()
        self._update_preview()

    def _update_preview(self, *_args) -> None:
        family = self.font_combo.currentFont().family()
        size = self.size_spin.value()
        color = self._color or "inherit"
        self.preview_label.setText(self.bot.tr("chat_appearance.preview"))
        self.preview_label.setStyleSheet(
            f"font-family: '{family}'; font-size: {size}pt; color: {color};"
        )

    def _save(self) -> None:
        self.bot.set_chat_appearance(
            font_family=self.font_combo.currentFont().family(),
            font_size=self.size_spin.value(),
            font_color=self._color,
        )
        self.accept()

    def result_appearance(self) -> dict:
        return self.bot.chat_appearance()
