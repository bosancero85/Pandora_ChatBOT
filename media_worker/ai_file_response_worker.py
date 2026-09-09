# -*- coding: utf-8 -*-
"""
ai_file_response_worker.py
-----------------------------
Bereitet eine angehängte Textdatei (z.B. .txt, .md, .py, .json, .csv) so
auf, dass sie als zusätzlicher Kontext in die nächste Chat-Nachricht
eingefügt werden kann. Binärdateien werden bewusst nicht eingelesen,
sondern nur mit Größe/Typ angekündigt.
"""

import os

TEXT_EXTENSIONS = {
    ".txt", ".md", ".py", ".json", ".csv", ".yaml", ".yml", ".xml",
    ".html", ".css", ".js", ".ini", ".cfg", ".log",
}
MAX_CHARS = 20_000


def build_file_context(path: str) -> str:
    """Liefert einen Textblock, der die Datei für den Chat-Kontext
    beschreibt bzw. (bei Textdateien) deren Inhalt enthält."""
    filename = os.path.basename(path)
    ext = os.path.splitext(path)[1].lower()

    if ext not in TEXT_EXTENSIONS:
        size_kb = os.path.getsize(path) / 1024 if os.path.isfile(path) else 0
        return f"[Angehängte Datei: {filename} ({size_kb:.1f} KB) - Binärformat, Inhalt nicht eingelesen]"

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read(MAX_CHARS + 1)
    except OSError as exc:
        return f"[Datei {filename} konnte nicht gelesen werden: {exc}]"

    truncated = len(content) > MAX_CHARS
    if truncated:
        content = content[:MAX_CHARS]

    header = f"[Inhalt der angehängten Datei '{filename}']"
    footer = "\n[... gekürzt ...]" if truncated else ""
    return f"{header}\n```\n{content}{footer}\n```"
