rule Role_00076_MeditationGuide {
    meta:
        description = "Erkennt System-Prompts für Achtsamkeitsübungen und Entspannungsanleitungen (kein Ersatz für psychotherapeutische Behandlung)"
        role_id = "role_00076"
        category = "Mindfulness"
        version = "1.0"

    strings:
        $sys_en = "You are a calm mindfulness guide who leads brief breathing and relaxation exercises, always noting this is not a substitute for professional mental health treatment" nocase
        $sys_de = "Du bist ein ruhiger Achtsamkeits-Guide, der kurze Atem- und Entspannungsuebungen anleitet und stets betont, dass dies keine psychotherapeutische Behandlung ersetzt" nocase

        $attr_1 = "breathing exercise" nocase
        $attr_2 = "Atemuebung" nocase

        $action_1 = "relaxation technique" nocase
        $action_2 = "Entspannungstechnik" nocase
        $action_3 = "not a substitute for therapy" nocase
        $action_4 = "ersetzt keine Psychotherapie" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
