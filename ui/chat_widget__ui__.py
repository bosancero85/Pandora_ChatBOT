# -*- coding: utf-8 -*-
"""
chat_widget__ui__.py
----------------------
Zentraler Chat-Bereich: scrollbarer Nachrichtenverlauf (MessageBubble je
Nachricht) plus Eingabezeile mit Senden/Stopp und Anhang-Buttons
(Datei/Bild/Video -> media_worker/*).
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QPushButton, QScrollArea, QTextEdit,
    QVBoxLayout, QWidget,
)

from ui.components.massage_bubble__ui__ import MessageBubble


class ChatWidget(QWidget):
    """Zeigt den Verlauf der aktuellen Session und nimmt neue Nachrichten
    entgegen."""

    message_sent = pyqtSignal(str)                 # reiner Nutzertext
    stop_requested = pyqtSignal()
    file_attached = pyqtSignal(str)                 # Pfad
    image_attached = pyqtSignal(str)                 # Pfad
    video_attached = pyqtSignal(str)                 # Pfad

    def __init__(self, chat_bot, parent=None):
        super().__init__(parent)
        self.bot = chat_bot
        self._streaming_bubble = None
        self._appearance = self.bot.chat_appearance()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_layout.addStretch(1)
        self.scroll_area.setWidget(self.messages_container)
        root.addWidget(self.scroll_area, 1)

        self.empty_label = QLabel()
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.messages_layout.insertWidget(0, self.empty_label)

        input_row = QHBoxLayout()
        input_row.setContentsMargins(8, 8, 8, 8)

        self.attach_file_btn = QPushButton("📎")
        self.attach_file_btn.clicked.connect(self._pick_file)
        input_row.addWidget(self.attach_file_btn)

        self.attach_image_btn = QPushButton("🖼")
        self.attach_image_btn.clicked.connect(self._pick_image)
        input_row.addWidget(self.attach_image_btn)

        self.attach_video_btn = QPushButton("🎬")
        self.attach_video_btn.clicked.connect(self._pick_video)
        input_row.addWidget(self.attach_video_btn)

        self.input_edit = QTextEdit()
        self.input_edit.setFixedHeight(64)
        input_row.addWidget(self.input_edit, 1)

        self.send_btn = QPushButton()
        self.send_btn.clicked.connect(self._on_send_clicked)
        input_row.addWidget(self.send_btn)

        self.stop_btn = QPushButton()
        self.stop_btn.clicked.connect(self.stop_requested.emit)
        self.stop_btn.setEnabled(False)
        input_row.addWidget(self.stop_btn)

        root.addLayout(input_row)

        self.retranslate_ui()

    # ------------------------------------------------------------------
    def retranslate_ui(self) -> None:
        tr = self.bot.tr
        self.input_edit.setPlaceholderText(tr("chat.placeholder"))
        self.send_btn.setText(tr("chat.send"))
        self.stop_btn.setText(tr("chat.stop"))
        self.attach_file_btn.setToolTip(tr("chat.attach.file"))
        self.attach_image_btn.setToolTip(tr("chat.attach.image"))
        self.attach_video_btn.setToolTip(tr("chat.attach.video"))
        self.empty_label.setText(tr("chat.empty"))

    # ------------------------------------------------------------------
    def _on_send_clicked(self) -> None:
        text = self.input_edit.toPlainText().strip()
        if not text:
            return
        self.input_edit.clear()
        self.message_sent.emit(text)

    def set_busy(self, busy: bool) -> None:
        self.send_btn.setEnabled(not busy)
        self.stop_btn.setEnabled(busy)
        self.input_edit.setEnabled(not busy)

    # ------------------------------------------------------------------
    # Nachrichten anzeigen
    # ------------------------------------------------------------------
    def clear_messages(self) -> None:
        while self.messages_layout.count() > 1:  # Stretch am Ende behalten
            item = self.messages_layout.takeAt(0)
            widget = item.widget()
            if widget is not None and widget is not self.empty_label:
                widget.deleteLater()
        self._streaming_bubble = None

    def load_history(self, messages) -> None:
        self.clear_messages()
        for msg in messages:
            self.add_message(msg.get("role", "user"), msg.get("content", ""))

    def add_message(self, role: str, text: str) -> MessageBubble:
        author = self.bot.tr("chat.you") if role == "user" else self.bot.tr("chat.assistant")
        bubble = MessageBubble(role, text, author, lm=self.bot.languages,
                                appearance=self._appearance)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)
        self._scroll_to_bottom()
        return bubble

    # ------------------------------------------------------------------
    # Darstellung (Schriftart/-größe/-farbe im Chattext)
    # ------------------------------------------------------------------
    def apply_appearance(self, appearance: dict) -> None:
        """Übernimmt neue Chat-Darstellungseinstellungen und wendet sie
        sofort auf alle bereits angezeigten Sprechblasen an."""
        self._appearance = dict(appearance or {})
        for i in range(self.messages_layout.count()):
            widget = self.messages_layout.itemAt(i).widget()
            if isinstance(widget, MessageBubble):
                widget.apply_appearance(self._appearance)

    def current_appearance(self) -> dict:
        return dict(self._appearance)

    def begin_streaming_response(self) -> None:
        self._streaming_bubble = self.add_message("assistant", "")

    def append_stream_chunk(self, chunk: str) -> None:
        if self._streaming_bubble is None:
            self.begin_streaming_response()
        self._streaming_bubble.append_chunk(chunk)
        self._scroll_to_bottom()

    def end_streaming_response(self) -> None:
        self._streaming_bubble = None

    def _scroll_to_bottom(self) -> None:
        bar = self.scroll_area.verticalScrollBar()
        bar.setValue(bar.maximum())

    # ------------------------------------------------------------------
    # Anhänge
    # ------------------------------------------------------------------
    def _pick_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, self.bot.tr("chat.attach.file"))
        if path:
            self.file_attached.emit(path)

    def _pick_image(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, self.bot.tr("chat.attach.image"),
            filter="Images (*.png *.jpg *.jpeg *.gif *.webp)",
        )
        if path:
            self.image_attached.emit(path)

    def _pick_video(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, self.bot.tr("chat.attach.video"),
            filter="Videos (*.mp4 *.mov *.mkv *.avi)",
        )
        if path:
            self.video_attached.emit(path)
