# -*- coding: utf-8 -*-
"""
loadingscreen__ui__.py
------------------------
Moderner Ladebildschirm mit selbst gezeichnetem "High-Glow"-Pandora®-Logo
(kein externes Bild-Asset nötig), einem Fortschrittsbalken und einer
darüber laufenden Liste der aktuell geladenen Rollen/Plugins/Tools -
alles wird direkt in ein QPixmap gerendert, das main.py bei jedem
Ladeschritt per ``show_step()``/``add_loaded_items()`` neu anfordert.
"""

import os

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QBrush, QColor, QFont, QLinearGradient, QPainter, QPainterPath, QPen,
    QPixmap, QRadialGradient,
)
from PyQt6.QtWidgets import QSplashScreen

WIDTH, HEIGHT = 560, 360
BG_TOP = QColor("#0d0d14")
BG_BOTTOM = QColor("#16121f")
VIOLET = QColor("#9d4edd")
CYAN = QColor("#00f0ff")
EMERALD = QColor("#10b981")
TEXT_MAIN = QColor("#f0f0f5")
TEXT_DIM = QColor("#8a8a9a")
MAX_VISIBLE_ITEMS = 6


from app.paths import get_project_root


def _project_root() -> str:
    return get_project_root()


def discover_loading_labels() -> dict:
    """Scannt ``plugins/`` und ``media_worker/`` nach Modulen, um sie
    während des Starts als 'werden geladen'-Liste anzuzeigen. Rein
    kosmetisch - die Module selbst werden ganz normal per Python-Import
    geladen, das hier liefert nur menschenlesbare Namen dafür."""
    root = _project_root()
    labels = {"plugins": [], "tools": []}

    plugins_dir = os.path.join(root, "plugins")
    if os.path.isdir(plugins_dir):
        for name in sorted(os.listdir(plugins_dir)):
            full = os.path.join(plugins_dir, name)
            if name.startswith("__"):
                continue
            if name.endswith(".py") and os.path.isfile(full):
                labels["plugins"].append(name[:-3].replace("_", " ").title())

    media_dir = os.path.join(root, "media_worker")
    if os.path.isdir(media_dir):
        for name in sorted(os.listdir(media_dir)):
            if name.endswith(".py") and not name.startswith("__"):
                labels["tools"].append(name[:-3].replace("_", " ").title())

    return labels


def _draw_glow_logo(painter: QPainter, center: QPointF, radius: float) -> None:
    """Zeichnet ein stilisiertes, leuchtendes Pandora®-Emblem: eine
    gedrehte Raute ('Box') mit weichem violett/cyan Halo und einem
    zentralen 'P'-Schriftzug - komplett vektoriell, kein Bild-Asset."""
    # Weicher äußerer Glow (mehrere transparente Kreise übereinander)
    for factor, alpha in ((2.4, 18), (1.9, 30), (1.5, 55), (1.15, 90)):
        glow = QRadialGradient(center, radius * factor)
        glow_color = QColor(VIOLET)
        glow_color.setAlpha(alpha)
        edge_color = QColor(VIOLET)
        edge_color.setAlpha(0)
        glow.setColorAt(0.0, glow_color)
        glow.setColorAt(1.0, edge_color)
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius * factor, radius * factor)

    # Rautenform (gedrehtes Quadrat) mit Verlauf violett -> cyan
    diamond = QPainterPath()
    diamond.moveTo(center + QPointF(0, -radius))
    diamond.lineTo(center + QPointF(radius, 0))
    diamond.lineTo(center + QPointF(0, radius))
    diamond.lineTo(center + QPointF(-radius, 0))
    diamond.closeSubpath()

    fill = QLinearGradient(center + QPointF(-radius, -radius), center + QPointF(radius, radius))
    fill.setColorAt(0.0, VIOLET)
    fill.setColorAt(1.0, CYAN)
    painter.setBrush(QBrush(fill))
    painter.setPen(QPen(QColor("#0d0d14"), 3))
    painter.drawPath(diamond)

    # Innerer Emerald-Akzentring
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(EMERALD, 2))
    painter.drawEllipse(center, radius * 0.55, radius * 0.55)

    # Zentrales 'P'-Monogramm
    font = QFont("Segoe UI", int(radius * 0.62), QFont.Weight.Black)
    painter.setFont(font)
    painter.setPen(QPen(QColor("#0d0d14")))
    text_rect = QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "P")


class LoadingScreen(QSplashScreen):
    """Ladebildschirm mit Logo, Fortschrittsbalken und Lade-Liste."""

    def __init__(self, chat_bot=None):
        self.bot = chat_bot
        self._message = "Pandora® ChatBot"
        self._progress = 0.0  # 0.0 - 1.0
        self._items: list = []

        super().__init__(self._render())
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _render(self) -> QPixmap:
        pixmap = QPixmap(WIDTH, HEIGHT)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # Hintergrund mit vertikalem Verlauf + abgerundeter Rahmen
        bg = QLinearGradient(0, 0, 0, HEIGHT)
        bg.setColorAt(0.0, BG_TOP)
        bg.setColorAt(1.0, BG_BOTTOM)
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, WIDTH, HEIGHT), 18, 18)
        painter.setClipPath(path)
        painter.fillPath(path, QBrush(bg))

        # Logo
        _draw_glow_logo(painter, QPointF(WIDTH / 2, 92), 46)

        # Titel / Untertitel
        painter.setPen(QPen(TEXT_MAIN))
        title_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.drawText(QRectF(0, 152, WIDTH, 34), Qt.AlignmentFlag.AlignCenter, "Pandora® ChatBot")

        painter.setPen(QPen(CYAN))
        subtitle_font = QFont("Segoe UI", 10)
        painter.setFont(subtitle_font)
        painter.drawText(QRectF(0, 184, WIDTH, 20), Qt.AlignmentFlag.AlignCenter, "by AKI_SystemDown®")

        # Liste der zuletzt geladenen Rollen/Plugins/Tools (über dem Balken)
        list_font = QFont("Segoe UI", 9)
        painter.setFont(list_font)
        visible_items = self._items[-MAX_VISIBLE_ITEMS:]
        list_top = 214
        line_height = 15
        for i, item in enumerate(visible_items):
            # Neuere Einträge (weiter unten in der Liste) etwas heller,
            # damit die Liste "hereinwächst" statt statisch zu wirken.
            fade = 0.45 + 0.55 * ((i + 1) / max(len(visible_items), 1))
            color = QColor(TEXT_DIM)
            color.setAlphaF(min(fade, 1.0))
            painter.setPen(QPen(color))
            painter.drawText(
                QRectF(40, list_top + i * line_height, WIDTH - 80, line_height),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                f"✓  {item}",
            )

        # Fortschrittsbalken
        bar_rect = QRectF(40, HEIGHT - 64, WIDTH - 80, 8)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#22222e"))
        painter.drawRoundedRect(bar_rect, 4, 4)

        fill_width = max(bar_rect.width() * max(0.0, min(self._progress, 1.0)), 8)
        fill_rect = QRectF(bar_rect.x(), bar_rect.y(), fill_width, bar_rect.height())
        fill_gradient = QLinearGradient(fill_rect.topLeft(), fill_rect.topRight())
        fill_gradient.setColorAt(0.0, VIOLET)
        fill_gradient.setColorAt(1.0, CYAN)
        painter.setBrush(QBrush(fill_gradient))
        painter.drawRoundedRect(fill_rect, 4, 4)

        # Status-Text unter dem Balken
        painter.setPen(QPen(TEXT_MAIN))
        status_font = QFont("Segoe UI", 10)
        painter.setFont(status_font)
        painter.drawText(
            QRectF(40, HEIGHT - 50, WIDTH - 80, 24),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            self._message,
        )
        painter.setPen(QPen(TEXT_DIM))
        painter.drawText(
            QRectF(40, HEIGHT - 50, WIDTH - 80, 24),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
            f"{int(round(self._progress * 100))}%",
        )

        painter.end()
        return pixmap

    def _refresh(self) -> None:
        self.setPixmap(self._render())

    # ------------------------------------------------------------------
    # Öffentliche API (von main.py aufgerufen)
    # ------------------------------------------------------------------
    def show_step(self, text: str, progress: float = None) -> None:
        self._message = text
        if progress is not None:
            self._progress = max(0.0, min(progress, 1.0))
        self._refresh()

    def show_step_key(self, key: str, default: str = "", progress: float = None) -> None:
        if self.bot is not None:
            text = self.bot.tr(key)
            self.show_step(text if text != key else (default or key), progress=progress)
        else:
            self.show_step(default or key, progress=progress)

    def add_loaded_items(self, items: list) -> None:
        """Hängt weitere 'fertig geladen'-Einträge an die Liste über dem
        Fortschrittsbalken an (z.B. Rollennamen, Plugin-/Tool-Namen)."""
        self._items.extend(str(i) for i in items if i)
        self._refresh()
