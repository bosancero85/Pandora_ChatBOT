# -*- coding: utf-8 -*-
"""
speech_to_txt.py
-------------------
Optionales Plugin: transkribiert eine Audiodatei zu Text, damit
gesprochene Nachrichten an den ChatBot geschickt werden können. Nutzt
``SpeechRecognition`` (Google Web Speech API als Standard-Backend) -
komplett optional, die App bleibt ohne installiertes Paket lauffähig.
"""

from typing import Optional

try:
    import speech_recognition as sr
except ImportError:
    sr = None


def transcribe_audio_file(path: str, language: str = "de-DE") -> Optional[str]:
    """Wandelt eine .wav-Datei in Text um. Gibt ``None`` zurück, wenn das
    Paket fehlt oder die Datei nicht erkannt werden konnte."""
    if sr is None:
        return None

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=language)
    except (sr.UnknownValueError, sr.RequestError, OSError):
        return None


def is_available() -> bool:
    return sr is not None
