# -*- coding: utf-8 -*-
"""
chat_bot.py
------------
Zentrale Orchestrierung des Pandora® ChatBot. Verbindet die vier
Kernkomponenten miteinander:

  - ConfigManager    -> unkritische Einstellungen (chatbot.cfg) und
                        sensible API-Keys je Anbieter (*.env)
  - LanguageManager  -> aktives Sprachpaket / Übersetzung
  - RoleManager      -> automatisch geladene KI-Rollen (Mehrfachauswahl)
  - MemoryWorker     -> persistierte Chat-Sessions

Die UI (``ui/main_window__ui__.py``) spricht ausschließlich mit dieser
Klasse und den einzelnen Provider-Workern (``core/*_worker.py``), nicht
direkt mit den Rohdateien.
"""

from typing import Dict, List, Optional

from assets.configs.config_manager import ConfigManager
from app.language_manager import LanguageManager
from app.role_manager import RoleManager
from core.memory_worker import MemoryWorker

PROVIDERS = ("claude", "gemini", "ollama")

# Anbieterspezifischer Env-Key für den API-Key/Host, wird von den
# Einstellungsfenstern UND den Workern gemeinsam genutzt.
SECRET_KEYS = {
    "claude": "CLAUDE_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "ollama": "OLLAMA_HOST",
}
DEFAULT_MODEL_KEYS = {
    "claude": ("CLAUDE_MODEL", "claude-sonnet-4-6"),
    "gemini": ("GEMINI_MODEL", "gemini-2.5-flash"),
    "ollama": ("OLLAMA_MODEL", "llama3.1"),
}


class ChatBot:
    """Fasst Konfiguration, Sprache, Rollen und Verlauf zu einer Fassade
    zusammen, über die die GUI arbeitet."""

    def __init__(self):
        self.config = ConfigManager()
        self.languages = LanguageManager(default_language=self.config.language)
        self.roles = RoleManager()
        self.memory = MemoryWorker()

        self.active_provider: str = self.config.active_provider or "gemini"
        self.selected_role_ids: List[str] = self.config.selected_role_ids
        self.current_session_id: Optional[str] = None

    # ------------------------------------------------------------------
    # Sprache
    # ------------------------------------------------------------------
    def tr(self, key: str, **kwargs) -> str:
        return self.languages.tr(key, **kwargs)

    def set_language(self, code: str) -> bool:
        ok = self.languages.set_language(code)
        if ok:
            self.config.language = code
        return ok

    # ------------------------------------------------------------------
    # Darstellung (Theme, Seitenleiste, Chat-Schrift)
    # ------------------------------------------------------------------
    @property
    def theme(self) -> str:
        return self.config.theme

    def set_theme(self, theme: str) -> None:
        self.config.theme = theme

    @property
    def sidebar_visible(self) -> bool:
        return self.config.sidebar_visible

    def set_sidebar_visible(self, visible: bool) -> None:
        self.config.sidebar_visible = visible

    def chat_appearance(self) -> Dict[str, object]:
        """Liefert die aktuell gespeicherten Chat-Darstellungseinstellungen
        (Schriftart, -größe, -farbe) als Dict für ``ChatWidget``/
        ``MessageBubble``."""
        return {
            "font_family": self.config.chat_font_family,
            "font_size": self.config.chat_font_size,
            "font_color": self.config.chat_font_color,
        }

    def set_chat_appearance(self, font_family: str = "", font_size: int = 13,
                             font_color: str = "") -> None:
        self.config.chat_font_family = font_family
        self.config.chat_font_size = font_size
        self.config.chat_font_color = font_color

    # ------------------------------------------------------------------
    # Anbieter
    # ------------------------------------------------------------------
    def set_active_provider(self, provider: str) -> None:
        if provider in PROVIDERS:
            self.active_provider = provider
            self.config.active_provider = provider

    def get_secret(self, provider: str) -> Optional[str]:
        key = SECRET_KEYS.get(provider)
        if not key:
            return None
        return self.config.get_secret(provider, key)

    def set_secret(self, provider: str, value: str) -> None:
        key = SECRET_KEYS.get(provider)
        if key:
            self.config.set_secret(provider, key, value)

    def get_model(self, provider: str) -> str:
        key, default = DEFAULT_MODEL_KEYS.get(provider, (None, ""))
        if key is None:
            return default
        return self.config.get_secret(provider, key, default) or default

    def set_model(self, provider: str, model: str) -> None:
        key, _default = DEFAULT_MODEL_KEYS.get(provider, (None, ""))
        if key:
            self.config.set_secret(provider, key, model)

    # ------------------------------------------------------------------
    # Rollen (Mehrfachauswahl)
    # ------------------------------------------------------------------
    def set_selected_roles(self, role_ids: List[str]) -> None:
        self.selected_role_ids = list(role_ids)
        self.config.selected_role_ids = self.selected_role_ids

    def build_system_prompt(self) -> str:
        """Kombiniert ausschließlich die aktuell ausgewählten Rollen
        (Mehrfachauswahl) zu einem System-Prompt in der aktiven Sprache."""
        return self.roles.build_system_prompt(
            self.selected_role_ids, language=self.languages.current_language
        )

    # ------------------------------------------------------------------
    # Sessions / Verlauf
    # ------------------------------------------------------------------
    def start_new_session(self, title: Optional[str] = None) -> str:
        title = title or self.tr("sidebar.sessions.new")
        session_id = self.memory.new_session(
            title=title, provider=self.active_provider,
            role_ids=self.selected_role_ids,
        )
        self.current_session_id = session_id
        return session_id

    def ensure_session(self) -> str:
        if not self.current_session_id:
            return self.start_new_session()
        return self.current_session_id

    def list_sessions(self) -> List[Dict]:
        return self.memory.list_sessions()

    def load_session(self, session_id: str) -> Optional[Dict]:
        data = self.memory.load_session(session_id)
        if data is not None:
            self.current_session_id = session_id
            self.selected_role_ids = data.get("role_ids", []) or self.selected_role_ids
            provider = data.get("provider")
            if provider in PROVIDERS:
                self.active_provider = provider
        return data

    def record_message(self, role: str, content: str) -> None:
        session_id = self.ensure_session()
        self.memory.append_message(session_id, role, content, provider=self.active_provider)

    def history_as_messages(self) -> List[Dict[str, str]]:
        """Liefert den bisherigen Verlauf der aktuellen Session im
        Format, das die Provider-Worker erwarten
        (``[{"role": "user"/"assistant", "content": "..."}]``)."""
        if not self.current_session_id:
            return []
        data = self.memory.load_session(self.current_session_id) or {}
        return [
            {"role": m["role"], "content": m["content"]}
            for m in data.get("messages", [])
            if m.get("role") in ("user", "assistant")
        ]
