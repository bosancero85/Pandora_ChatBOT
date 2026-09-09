# -*- coding: utf-8 -*-
"""
ollama_worker.py
-----------------
QThread-Worker, der eine Chat-Anfrage an einen lokalen (oder entfernten)
Ollama-Server schickt und die Antwort gestreamt über Qt-Signale an die GUI
zurückgibt. Anders als bei Claude/Gemini ist hier kein API-Key nötig -
stattdessen liegt die Server-Adresse in ``ollama.env``
(``ConfigManager.get_secret("ollama", "OLLAMA_HOST")``), da Ollama in der
Regel lokal ohne Zugangsdaten läuft.
"""

from PyQt6.QtCore import QThread, pyqtSignal

try:
    import ollama
except ImportError:  # Paket optional - App bleibt lauffähig, Worker meldet Fehler
    ollama = None

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1"


class OllamaWorker(QThread):
    """Führt eine einzelne Anfrage an Ollama in einem eigenen Thread aus."""

    chunk_received = pyqtSignal(str)      # einzelnes Textstück (Streaming)
    finished_response = pyqtSignal(str)   # vollständige Antwort am Ende
    error_occurred = pyqtSignal(str)      # menschenlesbare Fehlermeldung

    def __init__(self, host: str, messages: list, system_prompt: str = "",
                 model: str = DEFAULT_MODEL, parent=None):
        super().__init__(parent)
        self.host = host or DEFAULT_HOST
        self.messages = messages  # [{"role": "user"/"assistant", "content": "..."}]
        self.system_prompt = system_prompt or ""
        self.model = model or DEFAULT_MODEL
        self._stop_requested = False

    def stop(self) -> None:
        """Bricht das Streaming beim nächsten Chunk sauber ab."""
        self._stop_requested = True

    def run(self) -> None:
        if ollama is None:
            self.error_occurred.emit(
                "Das Paket 'ollama' ist nicht installiert. "
                "Bitte 'pip install ollama' ausführen."
            )
            return

        collected = []
        try:
            client = ollama.Client(host=self.host)
            chat_messages = []
            if self.system_prompt:
                chat_messages.append({"role": "system", "content": self.system_prompt})
            chat_messages.extend(self.messages)

            stream = client.chat(model=self.model, messages=chat_messages, stream=True)
            for part in stream:
                if self._stop_requested:
                    break
                text = part.get("message", {}).get("content", "")
                if text:
                    collected.append(text)
                    self.chunk_received.emit(text)
            self.finished_response.emit("".join(collected))
        except Exception as exc:  # bewusst breit, damit die GUI nie hängen bleibt
            self.error_occurred.emit(
                f"Ollama-Fehler: {exc} (läuft der Ollama-Server unter {self.host}?)"
            )
