# -*- coding: utf-8 -*-
"""
git_integration.py
---------------------
Leichte Wrapper-Funktionen um das lokal installierte ``git``-Kommando,
damit die App z.B. den Status eines Projektordners im Chat-Kontext
anzeigen kann. Nutzt bewusst kein GitPython, um keine zusätzliche
Pflichtabhängigkeit einzuführen - ``git`` selbst muss auf dem System
vorhanden sein.
"""

import subprocess
from typing import Optional


def _run_git(repo_path: str, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, *args],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return result.stderr.strip() or f"git {' '.join(args)} fehlgeschlagen."
        return result.stdout.strip()
    except FileNotFoundError:
        return "Git ist auf diesem System nicht installiert."
    except subprocess.TimeoutExpired:
        return "Git-Befehl hat zu lange gedauert (Timeout)."


def git_status(repo_path: str) -> str:
    return _run_git(repo_path, "status", "--short", "--branch")


def git_diff(repo_path: str, staged: bool = False) -> str:
    return _run_git(repo_path, "diff", "--staged" if staged else "--no-color")


def git_log(repo_path: str, limit: int = 10) -> str:
    return _run_git(repo_path, "log", f"-{limit}", "--oneline")


def git_commit(repo_path: str, message: str, add_all: bool = True) -> str:
    if add_all:
        add_result = _run_git(repo_path, "add", "-A")
        if add_result and "fehlgeschlagen" in add_result:
            return add_result
    return _run_git(repo_path, "commit", "-m", message)


def is_git_repo(repo_path: str) -> bool:
    output = _run_git(repo_path, "rev-parse", "--is-inside-work-tree")
    return output.strip() == "true"
