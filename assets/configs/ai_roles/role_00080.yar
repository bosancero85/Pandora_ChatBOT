rule Role_00080_ChessCoach {
    meta:
        description = "Erkennt System-Prompts für Schach-Eröffnungen, Taktiktraining und Partieanalyse"
        role_id = "role_00080"
        category = "Chess"
        version = "1.0"

    strings:
        $sys_en = "You are a chess coach who explains openings, tactical patterns and reviews games move by move" nocase
        $sys_de = "Du bist ein Schachtrainer, der Eroeffnungen, taktische Muster erklaert und Partien Zug fuer Zug analysiert" nocase

        $attr_1 = "opening theory" nocase
        $attr_2 = "Eroeffnungstheorie" nocase

        $action_1 = "tactical pattern" nocase
        $action_2 = "taktisches Muster" nocase
        $action_3 = "game analysis" nocase
        $action_4 = "Partieanalyse" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
