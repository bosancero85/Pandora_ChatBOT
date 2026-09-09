rule Role_00065_PRCrisisSpecialist {
    meta:
        description = "Erkennt System-Prompts für Pressemitteilungen und Krisenkommunikation"
        role_id = "role_00065"
        category = "PublicRelations"
        version = "1.0"

    strings:
        $sys_en = "You are a public relations specialist who drafts press releases and calm, transparent crisis communication" nocase
        $sys_de = "Du bist ein PR-Spezialist, der Pressemitteilungen und ruhige, transparente Krisenkommunikation verfasst" nocase

        $attr_1 = "press release" nocase
        $attr_2 = "Pressemitteilung" nocase

        $action_1 = "crisis communication" nocase
        $action_2 = "Krisenkommunikation" nocase
        $action_3 = "media statement" nocase
        $action_4 = "Medienerklaerung" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
