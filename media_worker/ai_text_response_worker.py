# -*- coding: utf-8 -*-
"""
ai_text_response_worker.py
-----------------------------
Kleine Factory, die für einen gegebenen Anbieter-Namen den passenden
Worker (``ClaudeWorker`` / ``GeminiWorker`` / ``OllamaWorker``) samt
seinen jeweiligen Konstruktor-Argumenten zurückgibt. Wird von
``ui/main_window__ui__.py`` genutzt, damit dort nicht anbieterspezifisch
verzweigt werden muss.
"""

from core.claude_worker import ClaudeWorker
from core.gemini_worker import GeminiWorker
from core.ollama_worker import OllamaWorker

_WORKER_CLASSES = {
    "claude": ClaudeWorker,
    "gemini": GeminiWorker,
    "ollama": OllamaWorker,
}


def create_text_worker(provider: str, secret: str, messages: list,
                        system_prompt: str = "", model: str = ""):
    """Erzeugt (aber startet noch nicht) den Worker für ``provider``.

    ``secret`` ist der API-Key (Claude/Gemini) bzw. die Server-Adresse
    (Ollama), jeweils frisch aus der passenden ``.env``-Datei gelesen."""
    worker_cls = _WORKER_CLASSES.get(provider)
    if worker_cls is None:
        raise ValueError(f"Unbekannter Anbieter: {provider}")

    kwargs = {"messages": messages, "system_prompt": system_prompt}
    if model:
        kwargs["model"] = model

    if provider == "ollama":
        return worker_cls(secret, **kwargs)
    return worker_cls(secret, **kwargs)
