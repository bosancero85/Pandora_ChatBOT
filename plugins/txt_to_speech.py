# -*- coding: utf-8 -*-
"""
txt_to_speech.py
-------------------
Optionales Plugin: liest eine Chat-Antwort offline per ``pyttsx3`` vor,
damit Antworten des ChatBots auch akustisch ausgegeben werden können.
Komplett optional, die App bleibt ohne installiertes Paket lauffähig.
"""

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

_engine = None


def _get_engine():
    global _engine
    if _engine is None and pyttsx3 is not None:
        _engine = pyttsx3.init()
    return _engine


def speak(text: str, rate: int = 180) -> bool:
    """Spricht ``text`` synchron aus. Gibt ``False`` zurück, wenn das
    Paket nicht installiert ist."""
    engine = _get_engine()
    if engine is None:
        return False
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()
    return True


def is_available() -> bool:
    return pyttsx3 is not None
