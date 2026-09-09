# -*- coding: utf-8 -*-
"""
language_manager.py
--------------------
Lädt die JSON-Sprachpakete aus ``assets/language_packs/`` und stellt die
komplette Mehrsprachigkeit des Pandora® ChatBot bereit.

Jedes Sprachpaket ist eine flache JSON-Datei mit einem ``_meta``-Block
(Sprachcode, Anzeigename, Flagge) und beliebig vielen ``"schluessel.pfad":
"Text"``-Einträgen. Neue Sprachen werden einfach als weitere ``<code>.json``
Datei in den Ordner gelegt - sie erscheinen automatisch in
``available_languages()``, ohne dass Code angepasst werden muss.

Fehlt ein Schlüssel in der aktiven Sprache, wird zuerst in der
Fallback-Sprache (Standard: Deutsch) und andernfalls beim Schlüssel selbst
nachgeschaut, damit die Oberfläche nie mit einer Exception abstürzt.
"""

import json
import os
from typing import Dict, Optional

try:
    from PyQt6.QtCore import QObject, pyqtSignal
    _HAS_QT = True
except ImportError:  # Erlaubt Nutzung/Tests auch ohne installiertes PyQt6
    _HAS_QT = False

    class QObject:  # type: ignore
        def __init__(self, *a, **kw):
            pass

    def pyqtSignal(*a, **kw):  # type: ignore
        class _DummySignal:
            def connect(self, *a, **kw):
                pass

            def emit(self, *a, **kw):
                pass

        return _DummySignal()


from app.paths import get_project_root

LANGUAGE_PACKS_DIR = os.path.join(get_project_root(), "assets", "language_packs")


class LanguageManager(QObject):
    """Zentrale Verwaltung aller Sprachpakete des ChatBots."""

    # Wird gefeuert, sobald sich die aktive Sprache ändert (neuer Code als str)
    language_changed = pyqtSignal(str)

    def __init__(self, packs_dir: Optional[str] = None,
                 default_language: str = "de", parent=None):
        super().__init__(parent)
        self.packs_dir = packs_dir or LANGUAGE_PACKS_DIR
        self.default_language = default_language
        self._current_code = default_language
        self._packs: Dict[str, dict] = {}
        self._meta: Dict[str, dict] = {}

        self.reload_available()

        # Falls die gewünschte Standardsprache fehlt, auf die erste
        # gefundene Sprache oder ein leeres Set zurückfallen.
        if default_language not in self._packs and self._packs:
            self._current_code = next(iter(self._packs))
        self.set_language(self._current_code, emit_signal=False)

    # ------------------------------------------------------------------
    # Laden
    # ------------------------------------------------------------------
    def reload_available(self) -> None:
        """Scannt den language_packs-Ordner neu nach *.json Dateien.

        Unterstützt zwei Layouts, damit neue Sprachen einfach per Ordner
        ODER per einzelner Datei ergänzt werden können:
          - flach:       assets/language_packs/de.json
          - je Ordner:   assets/language_packs/de_DE/de.json
        Beide Varianten werden rekursiv (eine Ebene tief) eingelesen."""
        self._packs.clear()
        self._meta.clear()

        if not os.path.isdir(self.packs_dir):
            os.makedirs(self.packs_dir, exist_ok=True)
            return

        json_paths = []
        for entry in sorted(os.listdir(self.packs_dir)):
            full = os.path.join(self.packs_dir, entry)
            if os.path.isfile(full) and entry.endswith(".json"):
                json_paths.append(full)
            elif os.path.isdir(full):
                for filename in sorted(os.listdir(full)):
                    if filename.endswith(".json"):
                        json_paths.append(os.path.join(full, filename))

        for path in json_paths:
            filename = os.path.basename(path)
            fallback_code = os.path.splitext(filename)[0]
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
            except (OSError, json.JSONDecodeError):
                continue

            meta = data.get("_meta", {})
            # Der Sprachcode aus dem _meta-Block hat Vorrang vor dem
            # Dateinamen, damit z.B. "de_DE/de.json" als "de" registriert
            # wird, auch wenn der Ordner anders benannt ist.
            code = meta.get("code", fallback_code)
            self._packs[code] = data
            self._meta[code] = {
                "code": code,
                "name": meta.get("name", code.upper()),
                "flag": meta.get("flag", ""),
            }

    def available_languages(self) -> Dict[str, dict]:
        """Liefert ``{"de": {"code": "de", "name": "Deutsch", "flag": "..."}}``."""
        return dict(self._meta)

    # ------------------------------------------------------------------
    # Aktive Sprache
    # ------------------------------------------------------------------
    @property
    def current_language(self) -> str:
        return self._current_code

    def set_language(self, code: str, emit_signal: bool = True) -> bool:
        """Wechselt die aktive Sprache. Gibt False zurück, falls das
        Sprachpaket nicht existiert (Sprache bleibt dann unverändert)."""
        if code not in self._packs:
            return False
        self._current_code = code
        if emit_signal:
            self.language_changed.emit(code)
        return True

    # ------------------------------------------------------------------
    # Übersetzen
    # ------------------------------------------------------------------
    def tr(self, key: str, **kwargs) -> str:
        """Übersetzt einen Schlüssel wie ``"chat.send"`` in den aktuell
        aktiven Sprachtext. Platzhalter im Text (``{provider}``) werden per
        ``str.format`` mit ``kwargs`` ersetzt. Fehlt der Schlüssel komplett,
        wird der Schlüssel selbst als sichtbarer Platzhalter zurückgegeben."""
        text = self._lookup(key)
        if text is None:
            return key
        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, IndexError):
                return text
        return text

    def _lookup(self, key: str) -> Optional[str]:
        pack = self._packs.get(self._current_code, {})
        if key in pack:
            return pack[key]

        fallback = self._packs.get(self.default_language, {})
        if key in fallback:
            return fallback[key]

        for pack in self._packs.values():
            if key in pack:
                return pack[key]
        return None

    # Kurzform, damit ui-Code `lm("chat.send")` statt `lm.tr("chat.send")`
    # schreiben kann, falls gewünscht.
    __call__ = tr