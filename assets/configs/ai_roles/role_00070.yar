rule Role_00070_InteriorDesignConsultant {
    meta:
        description = "Erkennt System-Prompts für Raumgestaltung, Farbkonzepte und Möblierungsvorschläge"
        role_id = "role_00070"
        category = "InteriorDesign"
        version = "1.0"

    strings:
        $sys_en = "You are an interior design consultant who suggests layouts, color palettes and furniture choices for a room" nocase
        $sys_de = "Du bist ein Innenarchitektur-Berater, der Raumaufteilungen, Farbkonzepte und Moeblierungsvorschlaege macht" nocase

        $attr_1 = "color palette" nocase
        $attr_2 = "Farbkonzept" nocase

        $action_1 = "room layout" nocase
        $action_2 = "Raumaufteilung" nocase
        $action_3 = "furniture choice" nocase
        $action_4 = "Moebelauswahl" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
