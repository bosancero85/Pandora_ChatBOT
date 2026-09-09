# -*- coding: utf-8 -*-
"""
main.py
--------
Einstiegspunkt des Pandora® ChatBot. Startet die QApplication, zeigt den
Ladebildschirm während Konfiguration/Sprache/Rollen initialisiert werden,
und öffnet danach das Hauptfenster.

Start:
    python main.py
"""

import os
import sys

# Erlaubt den Start sowohl per "python main.py" aus dem Projekt-Root als
# auch als installiertes Paket - das Projekt-Root wird immer zuerst im
# sys.path abgelegt, damit die absoluten Importe (app.*, core.*, ui.*)
# überall funktionieren.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from app.chat_bot import ChatBot
from app.paths import get_project_root
from ui.loadingscreen__ui__ import LoadingScreen, discover_loading_labels
from ui.main_window__ui__ import MainWindow

APP_ICON_PATH = os.path.join(get_project_root(), "assets", "icons", "pandora_chatbot.ico")


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Pandora® ChatBot")
    if os.path.isfile(APP_ICON_PATH):
        app.setWindowIcon(QIcon(APP_ICON_PATH))

    splash = LoadingScreen()
    splash.show()
    app.processEvents()

    splash.show_step_key("app.loading.config", "Konfiguration wird geladen …", progress=0.10)
    app.processEvents()
    bot = ChatBot()
    splash.add_loaded_items(["chatbot.cfg", "claude.env", "gemini.env", "ollama.env"])
    app.processEvents()

    splash.show_step_key("app.loading.language", "Sprachpaket wird geladen …", progress=0.30)
    app.processEvents()
    # bot.languages ist bereits in ChatBot.__init__ geladen worden.
    splash.add_loaded_items([
        f"{meta.get('flag', '')} {meta.get('name', code)}".strip()
        for code, meta in bot.languages.available_languages().items()
    ])
    app.processEvents()

    splash.show_step_key("app.loading.roles", "KI-Rollen werden geladen …", progress=0.55)
    app.processEvents()
    # bot.roles ist bereits in ChatBot.__init__ geladen worden.
    splash.add_loaded_items([role.display_name for role in bot.roles.list_roles()])
    app.processEvents()

    splash.show_step_key("app.loading.plugins", "Plugins & Tools werden geladen …", progress=0.78)
    app.processEvents()
    discovered = discover_loading_labels()
    splash.add_loaded_items(discovered["plugins"] + discovered["tools"])
    app.processEvents()

    splash.show_step_key("app.loading.ui", "Oberfläche wird aufgebaut …", progress=0.92)
    app.processEvents()
    window = MainWindow(bot)

    splash.show_step_key("app.loading.ui", "Oberfläche wird aufgebaut …", progress=1.0)
    app.processEvents()
    window.show()
    splash.finish(window)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
