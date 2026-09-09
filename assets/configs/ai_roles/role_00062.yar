rule Role_00062_InsuranceAdvisor {
    meta:
        description = "Erkennt System-Prompts für allgemeine Versicherungs-Erklärungen (kein Ersatz für eine lizenzierte Versicherungsberatung)"
        role_id = "role_00062"
        category = "Insurance"
        version = "1.0"

    strings:
        $sys_en = "You are an insurance guide who explains policy types and coverage terms in plain language, always noting this is not licensed insurance advice" nocase
        $sys_de = "Du bist ein Versicherungs-Ratgeber, der Policentypen und Deckungsbedingungen in einfacher Sprache erklaert und stets betont, dass dies keine lizenzierte Versicherungsberatung ersetzt" nocase

        $attr_1 = "coverage terms" nocase
        $attr_2 = "Deckungsbedingungen" nocase

        $action_1 = "policy comparison" nocase
        $action_2 = "Policenvergleich" nocase
        $action_3 = "deductible" nocase
        $action_4 = "Selbstbeteiligung" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
