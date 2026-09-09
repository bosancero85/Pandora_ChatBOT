# -*- coding: utf-8 -*-
"""
claude_worker.py
Automatisch erstellt mit Pandora® Structure Creator.
"""
# -*- coding: utf-8 -*-
"""
claude_worker.py
-----------------
QThread-Worker, der eine Chat-Anfrage an die Anthropic-API (Claude)
schickt und die Antwort gestreamt über Qt-Signale an die GUI zurückgibt.
Der API-Key wird nicht hier gespeichert, sondern kommt aus
``core.config_manager.ConfigManager.get_secret("claude", "CLAUDE_API_KEY")``
(claude.env) - der Worker bekommt ihn nur pro Aufruf übergeben.
"""

from PyQt6.QtCore import QThread, pyqtSignal

try:
    import anthropic
except ImportError:  # Paket optional - App bleibt lauffähig, Worker meldet Fehler
    anthropic = None

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_MAX_TOKENS = 4096


class ClaudeWorker(QThread):
    """Führt eine einzelne Anfrage an Claude in einem eigenen Thread aus."""

    chunk_received = pyqtSignal(str)      # einzelnes Textstück (Streaming)
    finished_response = pyqtSignal(str)   # vollständige Antwort am Ende
    error_occurred = pyqtSignal(str)      # menschenlesbare Fehlermeldung

    def __init__(self, api_key: str, messages: list, system_prompt: str = "",
                 model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS,
                 parent=None):
        super().__init__(parent)
        self.api_key = api_key
        self.messages = messages  # [{"role": "user"/"assistant", "content": "..."}]
        self.system_prompt = system_prompt or ""
        self.model = model or DEFAULT_MODEL
        self.max_tokens = max_tokens
        self._stop_requested = False

    def stop(self) -> None:
        """Bricht das Streaming beim nächsten Chunk sauber ab."""
        self._stop_requested = True

    def run(self) -> None:
        if anthropic is None:
            self.error_occurred.emit(
                "Das Paket 'anthropic' ist nicht installiert. "
                "Bitte 'pip install anthropic' ausführen."
            )
            return
        if not self.api_key:
            self.error_occurred.emit(
                "Kein Claude API-Key hinterlegt. Bitte in den "
                "Claude-Einstellungen speichern (wird in claude.env abgelegt)."
            )
            return

        collected = []
        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            with client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=self.messages,
            ) as stream:
                for text in stream.text_stream:
                    if self._stop_requested:
                        break
                    collected.append(text)
                    self.chunk_received.emit(text)
            self.finished_response.emit("".join(collected))
        except Exception as exc:  # bewusst breit, damit die GUI nie hängen bleibt
            self.error_occurred.emit(f"Claude-Fehler: {exc}")
