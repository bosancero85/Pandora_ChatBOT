rule Role_00046_MathTutor {
    meta:
        description = "Erkennt System-Prompts für Mathe-Nachhilfe mit Schritt-für-Schritt-Erklärungen"
        role_id = "role_00046"
        category = "Education"
        version = "1.0"

    strings:
        $sys_en = "You are a patient math tutor who explains problems step by step and checks understanding before moving on" nocase
        $sys_de = "Du bist ein geduldiger Mathe-Nachhilfelehrer, der Aufgaben Schritt fuer Schritt erklaert und das Verstaendnis prueft, bevor es weitergeht" nocase

        $attr_1 = "step by step" nocase
        $attr_2 = "Schritt fuer Schritt" nocase

        $action_1 = "practice problem" nocase
        $action_2 = "Uebungsaufgabe" nocase
        $action_3 = "check your work" nocase
        $action_4 = "Rechenweg pruefen" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
