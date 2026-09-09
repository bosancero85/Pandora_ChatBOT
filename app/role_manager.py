# -*- coding: utf-8 -*-
"""
role_manager.py
----------------
Lädt automatisch alle KI-Rollen aus ``assets/configs/ai_roles/*.yar``.

Die Rollen liegen als YARA-Regel-Dateien vor (Meta-Block für
role_id/description/category/version, Strings-Block mit den eigentlichen
System-Prompt-Fragmenten ``$sys_de`` / ``$sys_en``). Der RoleManager
benötigt dafür keine echte YARA-Engine - es werden nur Meta- und
Strings-Block per Regex ausgelesen, da die Regeln hier rein als
strukturierte Rollen-Container genutzt werden.

Neue Rollen werden einfach als weitere ``role_XXXXX.yar``-Datei in den
Ordner gelegt und erscheinen beim nächsten ``reload()`` automatisch in der
Mehrfachauswahl-Liste der Sidebar - ohne Codeänderung.
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.paths import get_project_root

ROLES_DIR = os.path.join(get_project_root(), "assets", "configs", "ai_roles")

_RULE_NAME_RE = re.compile(r"rule\s+(\w+)\s*{", re.IGNORECASE)
_META_BLOCK_RE = re.compile(r"meta:\s*(.*?)\s*strings:", re.DOTALL | re.IGNORECASE)
_STRINGS_BLOCK_RE = re.compile(r"strings:\s*(.*?)\s*condition:", re.DOTALL | re.IGNORECASE)
_KV_RE = re.compile(r'(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"')
_STRVAR_RE = re.compile(r'\$(\w+)\s*=\s*"((?:[^"\\]|\\.)*)"')


def _unescape(value: str) -> str:
    return value.replace('\\"', '"').replace("\\\\", "\\")


@dataclass
class Role:
    """Eine einzelne, aus einer .yar-Datei geladene KI-Rolle."""

    role_id: str
    rule_name: str
    name: str
    category: str
    description: str
    version: str
    prompts: Dict[str, str] = field(default_factory=dict)
    file_path: str = ""

    @property
    def display_name(self) -> str:
        """Menschenlesbarer Name, z.B. 'Developer' aus 'Role_00001_Developer'."""
        parts = self.rule_name.split("_", 2)
        return parts[2] if len(parts) == 3 else self.rule_name

    def prompt_for(self, language: str, fallback_order=("en", "de")) -> str:
        """Liefert das Prompt-Fragment für ``language``, sonst der Reihe
        nach die Sprachen aus ``fallback_order``, sonst das erste
        verfügbare Fragment."""
        if language in self.prompts:
            return self.prompts[language]
        for lang in fallback_order:
            if lang in self.prompts:
                return self.prompts[lang]
        return next(iter(self.prompts.values()), "")


class RoleManager:
    """Lädt und verwaltet alle verfügbaren Rollen aus ``ROLES_DIR``."""

    def __init__(self, roles_dir: Optional[str] = None):
        self.roles_dir = roles_dir or ROLES_DIR
        self._roles: Dict[str, Role] = {}
        self.reload()

    # ------------------------------------------------------------------
    def reload(self) -> None:
        """Scannt ``roles_dir`` neu nach ``*.yar``-Dateien."""
        self._roles.clear()

        if not os.path.isdir(self.roles_dir):
            os.makedirs(self.roles_dir, exist_ok=True)
            return

        for filename in sorted(os.listdir(self.roles_dir)):
            if not filename.lower().endswith(".yar"):
                continue
            path = os.path.join(self.roles_dir, filename)
            role = self._parse_role_file(path)
            if role is not None:
                self._roles[role.role_id] = role

    def _parse_role_file(self, path: str) -> Optional[Role]:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except OSError:
            return None

        rule_match = _RULE_NAME_RE.search(content)
        if not rule_match:
            return None
        rule_name = rule_match.group(1)

        meta_match = _META_BLOCK_RE.search(content)
        meta = {k: _unescape(v) for k, v in _KV_RE.findall(meta_match.group(1))} if meta_match else {}

        strings_match = _STRINGS_BLOCK_RE.search(content)
        prompts: Dict[str, str] = {}
        if strings_match:
            for var_name, value in _STRVAR_RE.findall(strings_match.group(1)):
                if var_name.startswith("sys_"):
                    lang_code = var_name[len("sys_"):]
                    prompts[lang_code] = _unescape(value)

        role_id = meta.get("role_id") or os.path.splitext(os.path.basename(path))[0]

        return Role(
            role_id=role_id,
            rule_name=rule_name,
            name=meta.get("category", rule_name) + " – " + rule_name,
            category=meta.get("category", "General"),
            description=meta.get("description", ""),
            version=meta.get("version", "1.0"),
            prompts=prompts,
            file_path=path,
        )

    # ------------------------------------------------------------------
    # Abfrage
    # ------------------------------------------------------------------
    def list_roles(self) -> List[Role]:
        """Alle Rollen, sortiert nach role_id - genau das, was die
        Mehrfachauswahl-Liste in der Sidebar zum Befüllen braucht."""
        return sorted(self._roles.values(), key=lambda r: r.role_id)

    def get_role(self, role_id: str) -> Optional[Role]:
        return self._roles.get(role_id)

    def categories(self) -> List[str]:
        return sorted({role.category for role in self._roles.values()})

    # ------------------------------------------------------------------
    # System-Prompt-Bau für mehrfach ausgewählte Rollen
    # ------------------------------------------------------------------
    def build_system_prompt(self, role_ids: List[str], language: str = "de",
                             separator: str = "\n\n") -> str:
        """Kombiniert die Prompt-Fragmente aller ausgewählten Rollen
        (Mehrfachauswahl) zu einem gemeinsamen System-Prompt in der
        gewünschten Sprache."""
        fragments = []
        for role_id in role_ids:
            role = self.get_role(role_id)
            if role is None:
                continue
            text = role.prompt_for(language)
            if text:
                fragments.append(text + ".")
        return separator.join(fragments)