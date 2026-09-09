# -*- coding: utf-8 -*-
"""
config_manager.py
------------------
Zentrale Konfigurationsverwaltung des Pandora® ChatBot. Trennt bewusst
zwei Arten von Daten:

1. SENSIBLE Daten (API-Keys, Tokens) -> je Anbieter eine eigene
   ``.env``-Datei unter ``assets/configs/ai_configs/`` (``claude.env``,
   ``gemini.env``, ``ollama.env``). Diese Dateien gehören NICHT ins Git
   (siehe ``.gitignore``) und werden nie in ``chatbot.cfg`` gespiegelt.

2. NORMALE Einstellungen (aktiver Anbieter, Sprache, ausgewählte Rollen,
   Fenstergröße) -> ``assets/configs/chatbot.cfg`` im INI-Format.

Damit lässt sich das ganze Projekt gefahrlos in ein Repository packen,
ohne dass versehentlich ein API-Key committet wird.
"""

import configparser
import os
from typing import Dict, List, Optional

try:
    from dotenv import dotenv_values, set_key
except ImportError:  # pragma: no cover - Fallback, falls python-dotenv fehlt
    dotenv_values = None
    set_key = None


# Der Projekt-Root wird zentral über app.paths.get_project_root() ermittelt
# (funktioniert sowohl im Quellcode-Betrieb als auch als PyInstaller-.exe,
# siehe build.bat). Vorher wurde BASE_DIR hier lokal über __file__
# berechnet - das führte nach einem Verschieben dieser Datei einmal zu
# einem doppelten "assets/assets"-Ordner (siehe Migration weiter unten).
from app.paths import get_project_root

BASE_DIR = get_project_root()
CONFIGS_DIR = os.path.join(BASE_DIR, "assets", "configs")
AI_CONFIGS_DIR = os.path.join(CONFIGS_DIR, "ai_configs")
CFG_PATH = os.path.join(CONFIGS_DIR, "chatbot.cfg")

ENV_FILES = {
    "claude": os.path.join(AI_CONFIGS_DIR, "claude.env"),
    "gemini": os.path.join(AI_CONFIGS_DIR, "gemini.env"),
    "ollama": os.path.join(AI_CONFIGS_DIR, "ollama.env"),
}

DEFAULT_CFG: Dict[str, Dict[str, str]] = {
    "general": {
        "language": "de",
        "active_provider": "gemini",
        "theme": "dark",
    },
    "roles": {
        "selected": "",
    },
    "window": {
        "width": "1280",
        "height": "800",
        "sidebar_visible": "1",
    },
    "chat_appearance": {
        # Leer = Standard aus dem aktiven Theme wird verwendet.
        "font_family": "",
        "font_size": "13",
        "font_color": "",
    },
}


class ConfigManager:
    """Liest/schreibt sowohl ``chatbot.cfg`` als auch die ``*.env``-Dateien."""

    def __init__(self, cfg_path: Optional[str] = None,
                 env_files: Optional[Dict[str, str]] = None):
        self.cfg_path = cfg_path or CFG_PATH
        self.env_files = env_files or ENV_FILES

        os.makedirs(os.path.dirname(self.cfg_path), exist_ok=True)
        os.makedirs(AI_CONFIGS_DIR, exist_ok=True)

        self._migrate_legacy_double_assets_bug()

        self._cfg = configparser.ConfigParser()
        self._load_cfg()
        self._ensure_env_files_exist()

    def _migrate_legacy_double_assets_bug(self) -> None:
        """Einmalige Selbstheilung für einen früheren Pfad-Bug: eine ältere
        Version dieser Datei berechnete BASE_DIR falsch und legte
        chatbot.cfg/*.env unsichtbar unter
        ``<Projekt-Root>/assets/assets/configs/...`` ab. Existiert dieser
        alte Ordner noch mit Inhalten, während die (jetzt korrekten) Pfade
        noch leer sind, werden die Dateien automatisch dorthin verschoben,
        damit bereits eingetragene API-Keys/Einstellungen nicht verloren
        gehen. Der doppelte Ordner wird danach entfernt."""
        legacy_configs_dir = os.path.join(BASE_DIR, "assets", "assets", "configs")
        if not os.path.isdir(legacy_configs_dir):
            return

        legacy_cfg = os.path.join(legacy_configs_dir, "chatbot.cfg")
        if os.path.isfile(legacy_cfg) and os.path.getsize(legacy_cfg) > 0 and (
            not os.path.isfile(self.cfg_path) or os.path.getsize(self.cfg_path) == 0
        ):
            os.replace(legacy_cfg, self.cfg_path)

        legacy_ai_configs_dir = os.path.join(legacy_configs_dir, "ai_configs")
        for provider, target_path in self.env_files.items():
            legacy_env = os.path.join(legacy_ai_configs_dir, os.path.basename(target_path))
            if os.path.isfile(legacy_env) and os.path.getsize(legacy_env) > 0 and (
                not os.path.isfile(target_path) or os.path.getsize(target_path) == 0
            ):
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                os.replace(legacy_env, target_path)

        # Aufräumen: den kompletten fehlerhaften Doppel-Ordner
        # "assets/assets" entfernen, sofern nach der Migration nichts
        # Wichtiges mehr darin übrig ist.
        legacy_assets_dir = os.path.join(BASE_DIR, "assets", "assets")
        try:
            import shutil
            shutil.rmtree(legacy_assets_dir, ignore_errors=True)
        except OSError:
            pass

    # ------------------------------------------------------------------
    # chatbot.cfg (unkritische Einstellungen)
    # ------------------------------------------------------------------
    def _load_cfg(self) -> None:
        if os.path.isfile(self.cfg_path) and os.path.getsize(self.cfg_path) > 0:
            self._cfg.read(self.cfg_path, encoding="utf-8")

        # Fehlende Sections/Keys mit sinnvollen Defaults auffüllen, ohne
        # bereits vorhandene, vom Nutzer gesetzte Werte zu überschreiben.
        changed = False
        for section, values in DEFAULT_CFG.items():
            if not self._cfg.has_section(section):
                self._cfg.add_section(section)
                changed = True
            for key, value in values.items():
                if not self._cfg.has_option(section, key):
                    self._cfg.set(section, key, value)
                    changed = True

        if changed or not os.path.isfile(self.cfg_path):
            self.save()

    def save(self) -> None:
        with open(self.cfg_path, "w", encoding="utf-8") as fh:
            self._cfg.write(fh)

    def get(self, section: str, key: str, fallback: str = "") -> str:
        return self._cfg.get(section, key, fallback=fallback)

    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        return self._cfg.getint(section, key, fallback=fallback)

    def set(self, section: str, key: str, value, save: bool = True) -> None:
        if not self._cfg.has_section(section):
            self._cfg.add_section(section)
        self._cfg.set(section, key, str(value))
        if save:
            self.save()

    # Komfort-Zugriffe für häufig gebrauchte Werte -----------------------
    @property
    def language(self) -> str:
        return self.get("general", "language", "de")

    @language.setter
    def language(self, code: str) -> None:
        self.set("general", "language", code)

    @property
    def active_provider(self) -> str:
        return self.get("general", "active_provider", "gemini")

    @active_provider.setter
    def active_provider(self, provider: str) -> None:
        self.set("general", "active_provider", provider)

    @property
    def selected_role_ids(self) -> List[str]:
        raw = self.get("roles", "selected", "")
        return [r for r in raw.split(",") if r]

    @selected_role_ids.setter
    def selected_role_ids(self, role_ids: List[str]) -> None:
        self.set("roles", "selected", ",".join(role_ids))

    @property
    def theme(self) -> str:
        return self.get("general", "theme", "dark")

    @theme.setter
    def theme(self, value: str) -> None:
        self.set("general", "theme", value)

    @property
    def sidebar_visible(self) -> bool:
        return self.get("window", "sidebar_visible", "1") != "0"

    @sidebar_visible.setter
    def sidebar_visible(self, visible: bool) -> None:
        self.set("window", "sidebar_visible", "1" if visible else "0")

    # -- Chat-Darstellung (Schriftart/-größe/-farbe) ----------------------
    @property
    def chat_font_family(self) -> str:
        return self.get("chat_appearance", "font_family", "")

    @chat_font_family.setter
    def chat_font_family(self, value: str) -> None:
        self.set("chat_appearance", "font_family", value or "")

    @property
    def chat_font_size(self) -> int:
        return self.get_int("chat_appearance", "font_size", 13)

    @chat_font_size.setter
    def chat_font_size(self, value: int) -> None:
        self.set("chat_appearance", "font_size", int(value))

    @property
    def chat_font_color(self) -> str:
        return self.get("chat_appearance", "font_color", "")

    @chat_font_color.setter
    def chat_font_color(self, value: str) -> None:
        self.set("chat_appearance", "font_color", value or "")

    # ------------------------------------------------------------------
    # *.env-Dateien (SENSIBLE Daten je KI-Anbieter)
    # ------------------------------------------------------------------
    def _ensure_env_files_exist(self) -> None:
        for path in self.env_files.values():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if not os.path.isfile(path):
                open(path, "a", encoding="utf-8").close()

    def get_secret(self, provider: str, key: str, default: Optional[str] = None) -> Optional[str]:
        """Liest einen Wert (z.B. API-Key) frisch aus ``<provider>.env``.

        Es wird bewusst nicht gecacht, damit ein extern (z.B. per Editor)
        geänderter Key ohne Neustart der App wirksam wird."""
        path = self.env_files.get(provider)
        if not path or not os.path.isfile(path):
            return default
        if dotenv_values is not None:
            values = dotenv_values(path)
        else:
            values = self._read_env_manual(path)
        value = values.get(key)
        return value if value else default

    def set_secret(self, provider: str, key: str, value: str) -> None:
        """Schreibt einen sensiblen Wert dauerhaft in die passende
        ``.env``-Datei des Anbieters (nicht in chatbot.cfg!)."""
        path = self.env_files.get(provider)
        if not path:
            raise ValueError(f"Unbekannter Anbieter: {provider}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.isfile(path):
            open(path, "a", encoding="utf-8").close()

        if set_key is not None:
            set_key(path, key, value, quote_mode="never")
        else:
            self._write_env_manual(path, key, value)

    def all_secrets(self, provider: str) -> Dict[str, str]:
        path = self.env_files.get(provider)
        if not path or not os.path.isfile(path):
            return {}
        if dotenv_values is not None:
            return dict(dotenv_values(path))
        return self._read_env_manual(path)

    # Minimaler Fallback, falls python-dotenv nicht installiert ist ------
    @staticmethod
    def _read_env_manual(path: str) -> Dict[str, str]:
        values: Dict[str, str] = {}
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip().strip('"')
        return values

    @staticmethod
    def _write_env_manual(path: str, key: str, value: str) -> None:
        values = ConfigManager._read_env_manual(path) if os.path.isfile(path) else {}
        values[key] = value
        with open(path, "w", encoding="utf-8") as fh:
            for k, v in values.items():
                fh.write(f"{k}={v}\n")