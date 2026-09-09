# -*- coding: utf-8 -*-
"""
memory_worker.py
-----------------
Persistiert Chat-Verläufe ("Sessions") lokal als JSON-Dateien, damit die
Sidebar eine Liste vergangener Chats anzeigen kann und ein Chat nach dem
Neustart der App weitergeführt werden kann. Bewusst getrennt vom
ConfigManager, da hier KEINE sensiblen Zugangsdaten liegen, sondern reine
Gesprächsinhalte.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from app.paths import get_project_root

DEFAULT_STORAGE_DIR = os.path.join(get_project_root(), "assets", "memory")


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


class MemoryWorker:
    """Verwaltet Sessions als je eine JSON-Datei unter ``storage_dir``."""

    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir or DEFAULT_STORAGE_DIR
        os.makedirs(self.storage_dir, exist_ok=True)

    # ------------------------------------------------------------------
    def _path_for(self, session_id: str) -> str:
        return os.path.join(self.storage_dir, f"{session_id}.json")

    def new_session(self, title: str = "Neuer Chat", provider: str = "",
                     role_ids: Optional[List[str]] = None) -> str:
        session_id = uuid.uuid4().hex[:12]
        data = {
            "id": session_id,
            "title": title,
            "provider": provider,
            "role_ids": role_ids or [],
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "messages": [],
        }
        self._write(session_id, data)
        return session_id

    def list_sessions(self) -> List[Dict]:
        """Liefert eine nach letzter Änderung sortierte Übersicht aller
        Sessions (ohne die vollen Nachrichten, für die Sidebar-Liste)."""
        sessions = []
        if not os.path.isdir(self.storage_dir):
            return sessions
        for filename in os.listdir(self.storage_dir):
            if not filename.endswith(".json"):
                continue
            data = self._read(filename[:-5])
            if data is None:
                continue
            sessions.append({
                "id": data.get("id"),
                "title": data.get("title", "Chat"),
                "provider": data.get("provider", ""),
                "updated_at": data.get("updated_at", ""),
                "message_count": len(data.get("messages", [])),
            })
        sessions.sort(key=lambda s: s.get("updated_at", ""), reverse=True)
        return sessions

    def load_session(self, session_id: str) -> Optional[Dict]:
        return self._read(session_id)

    def append_message(self, session_id: str, role: str, content: str,
                        provider: str = "") -> None:
        data = self._read(session_id)
        if data is None:
            return
        data["messages"].append({
            "role": role,  # "user" oder "assistant"
            "content": content,
            "provider": provider,
            "timestamp": _now_iso(),
        })
        data["updated_at"] = _now_iso()
        self._write(session_id, data)

    def rename_session(self, session_id: str, title: str) -> None:
        data = self._read(session_id)
        if data is None:
            return
        data["title"] = title
        data["updated_at"] = _now_iso()
        self._write(session_id, data)

    def delete_session(self, session_id: str) -> None:
        path = self._path_for(session_id)
        if os.path.isfile(path):
            os.remove(path)

    # ------------------------------------------------------------------
    def _read(self, session_id: str) -> Optional[Dict]:
        path = self._path_for(session_id)
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, json.JSONDecodeError):
            return None

    def _write(self, session_id: str, data: Dict) -> None:
        path = self._path_for(session_id)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)