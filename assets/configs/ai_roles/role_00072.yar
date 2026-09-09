rule Role_00072_GardeningAdvisor {
    meta:
        description = "Erkennt System-Prompts für Pflanzenpflege, Aussaatplanung und Gartengestaltung"
        role_id = "role_00072"
        category = "Gardening"
        version = "1.0"

    strings:
        $sys_en = "You are a gardening advisor who gives planting schedules and plant care tips suited to the season" nocase
        $sys_de = "Du bist ein Garten-Ratgeber, der Aussaatplaene und Pflanzenpflege-Tipps passend zur Jahreszeit gibt" nocase

        $attr_1 = "planting schedule" nocase
        $attr_2 = "Aussaatplan" nocase

        $action_1 = "plant care" nocase
        $action_2 = "Pflanzenpflege" nocase
        $action_3 = "soil type" nocase
        $action_4 = "Bodenart" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
