rule Role_00041_ContractAdvisor {
    meta:
        description = "Erkennt System-Prompts für allgemeine Vertrags- und Rechtsdokument-Unterstützung (kein Ersatz für anwaltliche Beratung)"
        role_id = "role_00041"
        category = "Legal"
        version = "1.0"

    strings:
        $sys_en = "You are a legal document assistant who explains contracts and legal texts in plain language, always noting this is not a substitute for a licensed lawyer" nocase
        $sys_de = "Du bist ein Rechtsdokument-Assistent, der Vertraege und juristische Texte in einfacher Sprache erklaert und stets darauf hinweist, dass dies keine Rechtsberatung durch einen Anwalt ersetzt" nocase

        $attr_1 = "plain language" nocase
        $attr_2 = "einfache Sprache" nocase

        $action_1 = "contract clause" nocase
        $action_2 = "Vertragsklausel" nocase
        $action_3 = "terms and conditions" nocase
        $action_4 = "Allgemeine Geschaeftsbedingungen" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
