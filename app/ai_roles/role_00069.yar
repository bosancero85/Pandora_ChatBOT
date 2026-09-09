rule Role_00069_Sommelier {
    meta:
        description = "Erkennt System-Prompts für Wein- und Speisebegleitung sowie Verkostungsnotizen"
        role_id = "role_00069"
        category = "WineCulinary"
        version = "1.0"

    strings:
        $sys_en = "You are a sommelier who suggests food and wine pairings and explains tasting notes in approachable terms" nocase
        $sys_de = "Du bist ein Sommelier, der Speise-Wein-Kombinationen vorschlaegt und Verkostungsnotizen verstaendlich erklaert" nocase

        $attr_1 = "tasting notes" nocase
        $attr_2 = "Verkostungsnotizen" nocase

        $action_1 = "wine pairing" nocase
        $action_2 = "Weinbegleitung" nocase
        $action_3 = "vintage" nocase
        $action_4 = "Jahrgang" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
