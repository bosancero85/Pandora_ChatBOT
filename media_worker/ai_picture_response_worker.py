# -*- coding: utf-8 -*-
"""
ai_picture_response_worker.py
--------------------------------
Wandelt eine angehängte Bilddatei in einen Base64-Content-Block um, der
den multimodalen Chat-APIs (aktuell: Claude) als Bild mitgegeben werden
kann. Gemini/Ollama-Unterstützung kann hier nach demselben Muster
ergänzt werden, sobald die jeweiligen Worker Bild-Inhalte entgegennehmen.
"""

import base64
import mimetypes
import os
from typing import Optional


def build_image_content_block(path: str) -> Optional[dict]:
    """Liefert einen Anthropic-kompatiblen Bild-Content-Block
    (``{"type": "image", "source": {...}}``) oder ``None`` bei Fehlern."""
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type or not mime_type.startswith("image/"):
        return None

    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None

    encoded = base64.b64encode(data).decode("ascii")
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": encoded,
        },
    }


def describe_image_for_context(path: str) -> str:
    """Textuelle Ankündigung für den Chatverlauf, wenn nur der aktive
    Anbieter kein Bild-Format unterstützt."""
    return f"[Angehängtes Bild: {os.path.basename(path)}]"
