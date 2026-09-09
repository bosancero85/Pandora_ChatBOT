rule Role_00074_AutomotiveAdvisor {
    meta:
        description = "Erkennt System-Prompts für allgemeine Auto-Wartungstipps und Kaufberatung (kein Ersatz für eine Werkstattdiagnose)"
        role_id = "role_00074"
        category = "Automotive"
        version = "1.0"

    strings:
        $sys_en = "You are an automotive advisor who explains maintenance basics and buying considerations, always noting this is not a substitute for a professional mechanic's diagnosis" nocase
        $sys_de = "Du bist ein Auto-Berater, der Wartungsgrundlagen und Kaufkriterien erklaert und stets betont, dass dies keine Werkstattdiagnose ersetzt" nocase

        $attr_1 = "maintenance schedule" nocase
        $attr_2 = "Wartungsplan" nocase

        $action_1 = "car buying tip" nocase
        $action_2 = "Kaufkriterium" nocase
        $action_3 = "not a substitute for a mechanic" nocase
        $action_4 = "ersetzt keine Werkstattdiagnose" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
