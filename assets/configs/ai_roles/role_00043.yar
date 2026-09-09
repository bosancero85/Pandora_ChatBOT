rule Role_00043_MarketingCopywriter {
    meta:
        description = "Erkennt System-Prompts für Werbetexte, Slogans und Marketing-Kampagnen"
        role_id = "role_00043"
        category = "Marketing"
        version = "1.0"

    strings:
        $sys_en = "You are a marketing copywriter who crafts persuasive, on-brand headlines, slogans and ad copy" nocase
        $sys_de = "Du bist ein Marketing-Texter, der ueberzeugende, markengerechte Headlines, Slogans und Werbetexte formulierst" nocase

        $attr_1 = "call to action" nocase
        $attr_2 = "Handlungsaufforderung" nocase

        $action_1 = "brand voice" nocase
        $action_2 = "Markenstimme" nocase
        $action_3 = "ad campaign" nocase
        $action_4 = "Werbekampagne" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
