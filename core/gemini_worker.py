# -*- coding: utf-8 -*-
"""
gemini_worker.py
-----------------
QThread-Worker, der eine Chat-Anfrage an die Google Gemini API schickt und
die Antwort gestreamt über Qt-Signale an die GUI zurückgibt. Der API-Key
wird nicht hier gespeichert, sondern kommt aus
``ConfigManager.get_secret("gemini", "GEMINI_API_KEY")`` (gemini.env) -
der Worker bekommt ihn nur pro Aufruf übergeben.
"""

from PyQt6.QtCore import QThread, pyqtSignal

try:
    from google import genai
except ImportError:  # Paket optional - App bleibt lauffähig, Worker meldet Fehler
    genai = None

DEFAULT_MODEL = "gemini-2.5-flash"


class GeminiWorker(QThread):
    """Führt eine einzelne Anfrage an Gemini in einem eigenen Thread aus."""

    chunk_received = pyqtSignal(str)      # einzelnes Textstück (Streaming)
    finished_response = pyqtSignal(str)   # vollständige Antwort am Ende
    error_occurred = pyqtSignal(str)      # menschenlesbare Fehlermeldung

    def __init__(self, api_key: str, messages: list, system_prompt: str = "",
                 model: str = DEFAULT_MODEL, parent=None):
        super().__init__(parent)
        self.api_key = api_key
        self.messages = messages  # [{"role": "user"/"assistant", "content": "..."}]
        self.system_prompt = system_prompt or ""
        self.model = model or DEFAULT_MODEL
        self._stop_requested = False

    def stop(self) -> None:
        """Bricht das Streaming beim nächsten Chunk sauber ab."""
        self._stop_requested = True

    @staticmethod
    def _to_gemini_history(messages: list) -> list:
        """Wandelt das interne ``user``/``assistant``-Format in das von
        Gemini erwartete ``user``/``model``-Format um.

        WICHTIG: Jeder Eintrag in ``parts`` muss ein Part-Objekt bzw. ein
        Dict mit ``"text"``-Schlüssel sein - ein roher String wie
        ``[msg["content"]]`` wird vom neuen 'google-genai'-SDK (pydantic-
        validiert) abgelehnt (siehe Bugfix: 'contents.list[...].Part.parts
        Input should be a valid dictionary'). Daher hier explizit als
        ``[{"text": ...}]`` verpackt."""
        history = []
        for msg in messages:
            role = "model" if msg.get("role") == "assistant" else "user"
            history.append({
                "role": role,
                "parts": [{"text": msg.get("content", "")}],
            })
        return history

    def run(self) -> None:
        if genai is None:
            self.error_occurred.emit(
                "Das Paket 'google-genai' ist nicht installiert. "
                "Bitte 'pip install google-genai' ausführen."
            )
            return
        if not self.api_key:
            self.error_occurred.emit(
                "Kein Gemini API-Key hinterlegt. Bitte in den "
                "Gemini-Einstellungen speichern (wird in gemini.env abgelegt)."
            )
            return

        collected = []
        try:
            client = genai.Client(api_key=self.api_key)
            history = self._to_gemini_history(self.messages)
            config = {"system_instruction": self.system_prompt} if self.system_prompt else None
            stream = client.models.generate_content_stream(
                model=self.model,
                contents=history,
                config=config,
            )
            for chunk in stream:
                if self._stop_requested:
                    break
                text = getattr(chunk, "text", None)
                if text:
                    collected.append(text)
                    self.chunk_received.emit(text)
            self.finished_response.emit("".join(collected))
        except Exception as exc:  # bewusst breit, damit die GUI nie hängen bleibt
            self.error_occurred.emit(f"Gemini-Fehler: {exc}")
