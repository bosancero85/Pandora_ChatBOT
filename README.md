# Pandora® ChatBot

Modularer Multi-Provider KI-Chat-Client (Claude, Gemini, Ollama) mit
automatisch geladenem Rollen-System (Mehrfachauswahl), vollständiger
Mehrsprachigkeit und sensiblen Zugangsdaten ausschließlich in
`.env`-Dateien.

## Start

```bash
pip install -r requirements.txt
python main.py
```

Beim ersten Start werden `assets/configs/chatbot.cfg` sowie leere
`assets/configs/ai_configs/{claude,gemini,ollama}.env`-Dateien
automatisch angelegt. Trage deine API-Keys über die Menüpunkte
**Einstellungen → Claude/Gemini/Ollama …** in der App ein - sie landen
dann ausschließlich in der jeweiligen `.env`-Datei, niemals in
`chatbot.cfg` und niemals im Git-Repository (siehe `.gitignore`).

## Windows-.exe bauen

```bat
install.bat   REM einmalig: virtuelle Umgebung + Abhängigkeiten
build.bat     REM erstellt dist\Pandora_ChatBot\Pandora_ChatBot.exe
```

`build.bat` baut per PyInstaller einen **--onedir**-Build (ein Ordner
mit `.exe` + allen Abhängigkeiten statt eines einzelnen
--onefile-Archivs - startet dadurch spürbar schneller), inklusive
`--collect-all` für PyQt6/anthropic/google.genai/ollama/dotenv/
SpeechRecognition/pyttsx3 sowie dem App-Icon unter
`assets/icons/pandora_chatbot.ico`. Der komplette Ordner
`dist\Pandora_ChatBot\` (nicht nur die `.exe`) wird zum
Weitergeben/Verschieben benötigt, da `assets/` (Sprachpakete, Rollen,
Konfiguration) direkt daneben liegt.

## Mehrsprachigkeit

Neue Sprache hinzufügen: einfach eine neue `<code>.json` nach dem
Schema von `assets/language_packs/de_DE/de.json` in einen neuen
Unterordner unter `assets/language_packs/` legen. Sie erscheint beim
nächsten Start automatisch in der Sprachauswahl der Seitenleiste -
ohne Codeänderung.

## Rollen (Mehrfachauswahl)

Neue KI-Rolle hinzufügen: eine weitere `role_XXXXX.yar`-Datei nach dem
Schema der vorhandenen Dateien unter `assets/configs/ai_roles/` ablegen.
Sie erscheint automatisch als weiterer Eintrag in der
Mehrfachauswahl-Liste der Seitenleiste. Alle angehakten Rollen werden zu
einem gemeinsamen System-Prompt kombiniert (`RoleManager.build_system_prompt`).

## Projektstruktur (Kurzüberblick)

```
main.py                        Einstiegspunkt
app/
  chat_bot.py                  Orchestrator (Config, Sprache, Rollen, Verlauf)
  language_manager.py          Lädt assets/language_packs/*
  role_manager.py              Lädt assets/configs/ai_roles/*.yar
core/
  claude_worker.py / gemini_worker.py / ollama_worker.py
  memory_worker.py             Chat-Verläufe als JSON
ui/
  main_window__ui__.py, chat_widget__ui__.py, ...
  components/sidebar__ui__.py, massage_bubble__ui__.py
media_worker/                  Datei-/Bild-/Video-Anhänge, Terminal
plugins/                       Git-Integration, Speech-to-Text, Text-to-Speech
assets/
  configs/                     chatbot.cfg (unkritisch) + ai_configs/*.env (sensibel)
  language_packs/               Sprachpakete
```

## Changelog (dieser Durchlauf)

- **Bugfix Gemini:** `contents`/`parts` mussten für das neue `google-genai`-SDK
  als `{"text": "..."}`-Dicts übergeben werden statt als rohe Strings
  (`core/gemini_worker.py`).
- **Bugfix doppelter Ordner:** `assets/configs/config_manager.py` berechnete
  nach dem Verschieben der Datei den Projekt-Root falsch, wodurch
  `assets/assets/configs/...` entstand und API-Keys/Einstellungen dort
  "unsichtbar" landeten. Fix inkl. automatischer einmaliger Migration
  bereits gespeicherter Werte beim nächsten Start.
- **Ladebildschirm:** komplett neu, mit selbst gezeichnetem Glow-Logo
  (kein Bild-Asset nötig), Fortschrittsbalken und einer mitlaufenden
  Liste der geladenen Sprachen/Rollen/Plugins/Tools.
- **Hilfe:** `help_window__ui__.py` zeigt jetzt zwei Tabs - "Einrichtung"
  (Kurzanleitung) und "API-Keys" (Schritt-für-Schritt je Anbieter inkl.
  Button zum Öffnen der jeweiligen Anbieter-Seite). Alle Texte kommen aus
  den Sprachpaketen.
- **Neu:** `disclaimer_window__ui__.py` und `license_window__ui__.py`,
  beide über das Hilfe-Menü erreichbar, ebenfalls vollständig
  mehrsprachig über die JSON-Sprachpakete.
- **Entfernt (auf Wunsch):** Die komplette Pandora<#>-Skriptsprache
  (`plugins/pandora_hash/`, Beispiele, `core/pandora_hash_translator_worker.py`,
  `app/pandora_hash_plugin.py`) sowie die zugehörige feste
  "nur Pandora<#> zum Coden"-Systemprompt-Direktive wurden vollständig
  entfernt. Der ChatBot nutzt für Coding-Aufgaben jetzt wieder
  ausschließlich die normalen, per Mehrfachauswahl gewählten
  Rollen-Prompts - keine zusätzliche, immer aktive Zwangsregel mehr.
  Die "Code ausführen"-Schaltfläche an Chat-Nachrichten wurde ebenfalls
  entfernt, da sie ausschließlich für Pandora<#> gedacht war.
- **Windows-.exe:** `build.bat` (PyInstaller --onedir, --collect-all,
  App-Icon) und `install.bat` (virtuelle Umgebung einrichten) hinzugefügt.
  Neues Icon unter `assets/icons/pandora_chatbot.ico` (passend zum
  Ladebildschirm-Design). Alle Pfad-Berechnungen (`config_manager.py`,
  `language_manager.py`, `role_manager.py`, `memory_worker.py`,
  `loadingscreen__ui__.py`) laufen jetzt zentral über
  `app/paths.py::get_project_root()`, das zwischen normalem
  Python-Betrieb und PyInstaller-.exe (`sys.frozen`) unterscheidet -
  vorher hätten diese Pfade in einer gebauten .exe ins Leere gezeigt.

