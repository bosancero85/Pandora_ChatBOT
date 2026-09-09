rule Role_00000_CustomerSupport {
    meta:
        description = "Erkennt System-Prompts und Signaturen für Kundensupport-Rollen"
        role_id = "role_00000"
        category = "Support"
        version = "1.0"

    strings:
        $sys_en = "You are a helpful customer support representative" nocase
        $sys_de = "Du bist ein freundlicher Kundenservice-Mitarbeiter" nocase
        
        $attr_1 = "polite tone" nocase
        $attr_2 = "professioneller Ton" nocase
        
        $action_1 = "resolve ticket" nocase
        $action_2 = "Hilfe bei Bestellungen" nocase
        $action_3 = "frequently asked questions" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or any of ($action_*))
}