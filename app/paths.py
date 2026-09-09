# -*- coding: utf-8 -*-
"""
paths.py
------------
Zentrale, PyInstaller-sichere Ermittlung des Projekt-Root-Verzeichnisses.

Im normalen Python-Betrieb (``python main.py``) lässt sich der Root
einfach über ``__file__`` der aufrufenden Datei berechnen. Sobald die App
aber mit PyInstaller zu einer .exe gebaut wurde (``build.bat``), liegen
alle .py-Module nur noch komprimiert im PYZ-Archiv - ``__file__`` zeigt
dann NICHT mehr zuverlässig auf einen echten Ordner neben ``assets/``.

``get_project_root()`` erkennt diesen Fall über ``sys.frozen`` und nutzt
stattdessen den Ordner der .exe selbst (im --onedir-Modus liegt
``assets/`` dort direkt daneben, siehe ``build.bat`` -> ``--add-data``).
Alle Module, die Pfade unter ``assets/`` berechnen (config_manager,
language_manager, role_manager, memory_worker, loadingscreen), nutzen
diese eine Funktion, damit sich das Verhalten nur an einer Stelle pflegen
lässt.
"""

import os
import sys


def get_project_root() -> str:
    """Liefert das Projekt-Root-Verzeichnis - sowohl im Quellcode-Betrieb
    als auch als PyInstaller-.exe (--onedir)."""
    if getattr(sys, "frozen", False):
        # PyInstaller --onedir: die .exe liegt im Root der dist-Ordner-
        # Struktur, "assets/" wird per --add-data direkt daneben gelegt.
        return os.path.dirname(sys.executable)

    # Normaler Python-Betrieb: von dieser Datei (app/paths.py) aus eine
    # Ebene hoch = Projekt-Root.
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
