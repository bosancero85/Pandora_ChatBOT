rule Role_00068_EtiquetteAdvisor {
    meta:
        description = "Erkennt System-Prompts für Umgangsformen, Business-Etikette und interkulturelle Höflichkeitsregeln"
        role_id = "role_00068"
        category = "Etiquette"
        version = "1.0"

    strings:
        $sys_en = "You are an etiquette advisor who explains polite conventions for business, dining and cross-cultural situations" nocase
        $sys_de = "Du bist ein Etikette-Berater, der hoefliche Umgangsformen fuer Business, Tischsitten und interkulturelle Situationen erklaert" nocase

        $attr_1 = "dining etiquette" nocase
        $attr_2 = "Tischsitten" nocase

        $action_1 = "business etiquette" nocase
        $action_2 = "Business-Etikette" nocase
        $action_3 = "cultural norm" nocase
        $action_4 = "kulturelle Norm" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
