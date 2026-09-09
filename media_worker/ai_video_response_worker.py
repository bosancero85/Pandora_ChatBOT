# -*- coding: utf-8 -*-
"""
ai_video_response_worker.py
------------------------------
Video-Anhänge werden aktuell von keinem der drei angebundenen Anbieter
(Claude, Gemini-Textmodus, Ollama) direkt verarbeitet. Dieses Modul
liefert daher nur eine saubere Ankündigung für den Chatverlauf, statt
stillschweigend nichts zu tun - so weiß der Nutzer, dass die Datei
angehängt, aber nicht inhaltlich ausgewertet wurde.
"""

import os


def describe_video_for_context(path: str) -> str:
    size_mb = os.path.getsize(path) / (1024 * 1024) if os.path.isfile(path) else 0
    return (
        f"[Angehängtes Video: {os.path.basename(path)} ({size_mb:.1f} MB) - "
        "Videoinhalte werden aktuell nicht ausgewertet, nur der Dateiname "
        "wird als Kontext übergeben.]"
    )
