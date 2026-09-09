rule Role_00012_UIUXDesigner {
    meta:
        description = "Erkennt System-Prompts für UI/UX-Design, QSS-Styling und Layout-Optimierung"
        role_id = "role_00012"
        category = "Frontend"
        version = "1.0"

    strings:
        $sys_en = "You are a UI/UX designer" nocase
        $sys_de = "Du agierst als spezialisierter UI/UX-Designer" nocase

        $ui_1 = "QSS" nocase
        $ui_2 = "Qt Style Sheets" nocase
        $ui_3 = "QVBoxLayout" nocase
        $ui_4 = "Cyberpunk" nocase
        $ui_5 = "responsive layout" nocase

    condition:
        any of ($sys_*) and 2 of ($ui_*)
}

