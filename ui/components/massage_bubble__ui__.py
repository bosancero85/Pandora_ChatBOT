# -*- coding: utf-8 -*-
"""
massage_bubble__ui__.py
------------------------
Einzelne Chat-Sprechblase (Nutzer rechts, Assistent links) mit einer
"Kopieren"-Schaltfläche für den vollständigen Nachrichtentext.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget,
)


class MessageBubble(QFrame):
    """Eine einzelne Chat-Nachricht als Sprechblase."""

    def __init__(self, role: str, text: str, author_label: str, lm=None,
                 appearance: dict = None, parent=None):
        super().__init__(parent)
        self.role = role  # "user" oder "assistant"
        self.lm = lm
        self._full_text = ""

        self.setObjectName("MessageBubble")
        self.setFrameShape(QFrame.Shape.NoFrame)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(8, 4, 8, 4)

        bubble = QFrame()
        bubble.setObjectName("BubbleUser" if role == "user" else "BubbleAssistant")
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(12, 8, 12, 8)
        bubble_layout.setSpacing(4)

        self.author_label = QLabel(author_label)
        self.author_label.setObjectName("BubbleAuthor")
        bubble_layout.addWidget(self.author_label)

        self.text_label = QLabel()
        self.text_label.setWordWrap(True)
        self.text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.text_label.setObjectName("BubbleText")
        bubble_layout.addWidget(self.text_label)

        actions_row = QHBoxLayout()
        self.copy_button = QPushButton(self._tr("chat.copy", "Kopieren"))
        self.copy_button.setFlat(True)
        self.copy_button.clicked.connect(self._copy_to_clipboard)
        actions_row.addWidget(self.copy_button)
        actions_row.addStretch(1)
        bubble_layout.addLayout(actions_row)

        bubble.setMaximumWidth(720)
        bubble.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        if role == "user":
            outer.addStretch(1)
            outer.addWidget(bubble)
        else:
            outer.addWidget(bubble)
            outer.addStretch(1)

        self.set_text(text)
        self.apply_appearance(appearance or {})

    # ------------------------------------------------------------------
    # Darstellung (Schriftart/-größe/-farbe im Chattext)
    # ------------------------------------------------------------------
    def apply_appearance(self, appearance: dict) -> None:
        """Wendet Schriftart/-größe/-farbe auf den Nachrichtentext an.
        Leere Werte ('') übernehmen weiterhin den Stil aus dem aktiven
        Theme-Stylesheet (kein Override)."""
        font_family = (appearance or {}).get("font_family") or ""
        font_size = (appearance or {}).get("font_size") or 0
        font_color = (appearance or {}).get("font_color") or ""

        style_parts = []
        if font_family:
            style_parts.append(f"font-family: '{font_family}';")
        if font_size:
            style_parts.append(f"font-size: {int(font_size)}pt;")
        if font_color:
            style_parts.append(f"color: {font_color};")

        self.text_label.setStyleSheet(
            "#BubbleText { " + " ".join(style_parts) + " }" if style_parts else ""
        )

    # ------------------------------------------------------------------
    def _tr(self, key: str, default: str) -> str:
        if self.lm is not None:
            value = self.lm.tr(key)
            return value if value != key else default
        return default

    def _copy_to_clipboard(self) -> None:
        QApplication.clipboard().setText(self._full_text)

    # ------------------------------------------------------------------
    def set_text(self, text: str) -> None:
        """Setzt den vollständigen Text (für gestreamte Antworten laufend
        aufgerufen)."""
        self._full_text = text
        self.text_label.setText(text)

    def append_chunk(self, chunk: str) -> None:
        """Hängt ein gestreamtes Textstück an (für laufende Antworten)."""
        self.set_text(self._full_text + chunk)
