rule Role_00075_PetCareAdvisor {
    meta:
        description = "Erkennt System-Prompts für allgemeine Haustierpflege (kein Ersatz für eine tierärztliche Untersuchung)"
        role_id = "role_00075"
        category = "PetCare"
        version = "1.0"

    strings:
        $sys_en = "You are a pet care advisor who gives general feeding, training and enrichment tips, always noting this is not a substitute for veterinary examination" nocase
        $sys_de = "Du bist ein Haustier-Berater, der allgemeine Tipps zu Fuetterung, Training und Beschaeftigung gibt und stets betont, dass dies keine tieraerztliche Untersuchung ersetzt" nocase

        $attr_1 = "training tip" nocase
        $attr_2 = "Trainingstipp" nocase

        $action_1 = "feeding schedule" nocase
        $action_2 = "Fuetterungsplan" nocase
        $action_3 = "not a substitute for veterinary care" nocase
        $action_4 = "ersetzt keine tieraerztliche Untersuchung" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
