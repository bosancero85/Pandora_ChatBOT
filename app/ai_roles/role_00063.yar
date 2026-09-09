rule Role_00063_TaxPrepHelper {
    meta:
        description = "Erkennt System-Prompts für allgemeine Steuererklärungs-Orientierung (kein Ersatz für einen Steuerberater)"
        role_id = "role_00063"
        category = "Taxation"
        version = "1.0"

    strings:
        $sys_en = "You are a tax filing helper who explains general tax concepts and common deductions, always noting this is not a substitute for a licensed tax advisor" nocase
        $sys_de = "Du bist ein Steuererklaerungs-Helfer, der allgemeine Steuerkonzepte und gaengige Absetzbetraege erklaert und stets betont, dass dies keinen Steuerberater ersetzt" nocase

        $attr_1 = "tax deduction" nocase
        $attr_2 = "Absetzbetrag" nocase

        $action_1 = "filing deadline" nocase
        $action_2 = "Abgabefrist" nocase
        $action_3 = "tax bracket" nocase
        $action_4 = "Steuerklasse" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
