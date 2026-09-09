rule Role_00048_Storyteller {
    meta:
        description = "Erkennt System-Prompts für fiktionale Kurzgeschichten und Erzählungen"
        role_id = "role_00048"
        category = "Creative"
        version = "1.0"

    strings:
        $sys_en = "You are a creative storyteller who writes vivid short fiction with strong characters and atmosphere" nocase
        $sys_de = "Du bist ein kreativer Geschichtenerzaehler, der lebendige Kurzgeschichten mit starken Charakteren und Atmosphaere schreibst" nocase

        $attr_1 = "vivid imagery" nocase
        $attr_2 = "lebendige Bilder" nocase

        $action_1 = "character arc" nocase
        $action_2 = "Charakterentwicklung" nocase
        $action_3 = "short story" nocase
        $action_4 = "Kurzgeschichte" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
