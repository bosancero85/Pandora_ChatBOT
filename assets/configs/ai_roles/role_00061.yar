rule Role_00061_RealEstateAdvisor {
    meta:
        description = "Erkennt System-Prompts für Immobiliensuche, Exposé-Texte und Kauf-/Mietberatung (kein Ersatz für einen Makler oder Notar)"
        role_id = "role_00061"
        category = "RealEstate"
        version = "1.0"

    strings:
        $sys_en = "You are a real estate advisor who helps evaluate listings, writes property descriptions and explains buying or renting basics, always noting this is not a substitute for a licensed realtor or notary" nocase
        $sys_de = "Du bist ein Immobilienberater, der Angebote einschaetzt, Exposé-Texte schreibt und Kauf- oder Mietgrundlagen erklaert und stets betont, dass dies keinen Makler oder Notar ersetzt" nocase

        $attr_1 = "property listing" nocase
        $attr_2 = "Immobilienangebot" nocase

        $action_1 = "exposé text" nocase
        $action_2 = "Exposé-Text" nocase
        $action_3 = "rent or buy" nocase
        $action_4 = "mieten oder kaufen" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
