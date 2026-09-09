# -*- coding: utf-8 -*-
"""
ai_terminal_coworker.py
--------------------------
Führt einen einzelnen, vom Nutzer explizit eingegebenen Shell-Befehl in
einem eigenen Thread aus und streamt stdout/stderr zurück - gedacht als
kleines "Terminal neben dem Chat" für lokale Entwicklungsaufgaben (z.B.
schnell ein Skript testen, das die KI gerade vorgeschlagen hat).

WICHTIG: Der Befehl wird ausschließlich lokal und nur nach expliziter
Bestätigung durch den Nutzer ausgeführt - die KI-Antwort selbst startet
hier nichts automatisch.
"""

import subprocess

from PyQt6.QtCore import QThread, pyqtSignal


class TerminalCoworker(QThread):
    """Führt ``command`` in einer Shell aus und meldet die Ausgabe."""

    output_received = pyqtSignal(str)
    finished_with_code = pyqtSignal(int)
    error_occurred = pyqtSignal(str)

    def __init__(self, command: str, cwd: str = None, parent=None):
        super().__init__(parent)
        self.command = command
        self.cwd = cwd
        self._process = None

    def stop(self) -> None:
        if self._process is not None and self._process.poll() is None:
            self._process.terminate()

    def run(self) -> None:
        if not self.command.strip():
            self.error_occurred.emit("Kein Befehl angegeben.")
            return
        try:
            self._process = subprocess.Popen(
                self.command,
                cwd=self.cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            for line in self._process.stdout:
                self.output_received.emit(line)
            self._process.wait()
            self.finished_with_code.emit(self._process.returncode)
        except Exception as exc:
            self.error_occurred.emit(f"Terminal-Fehler: {exc}")
