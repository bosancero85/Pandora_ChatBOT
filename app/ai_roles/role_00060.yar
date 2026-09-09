rule Role_00060_GameMasterNarrator {
    meta:
        description = "Erkennt System-Prompts für einen Pen-and-Paper-Spielleiter (Tabletop-RPG-Erzähler)"
        role_id = "role_00060"
        category = "TabletopGaming"
        version = "1.0"

    strings:
        $sys_en = "You are a tabletop RPG game master who narrates vivid scenes and adapts the story to the players' choices" nocase
        $sys_de = "Du bist ein Pen-and-Paper-Spielleiter, der lebendige Szenen erzaehlt und die Geschichte an die Entscheidungen der Spieler anpasst" nocase

        $attr_1 = "non-player character" nocase
        $attr_2 = "Nichtspielercharakter" nocase

        $action_1 = "dice roll" nocase
        $action_2 = "Wurfergebnis" nocase
        $action_3 = "quest hook" nocase
        $action_4 = "Abenteuerhaken" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
