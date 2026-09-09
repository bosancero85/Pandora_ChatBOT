rule Role_00067_PublicSpeakingCoach {
    meta:
        description = "Erkennt System-Prompts für Redenschreiben, Präsentationsaufbau und Lampenfieber-Tipps"
        role_id = "role_00067"
        category = "PublicSpeaking"
        version = "1.0"

    strings:
        $sys_en = "You are a public speaking coach who structures speeches and gives tips for confident delivery and stage presence" nocase
        $sys_de = "Du bist ein Redecoach, der Reden strukturiert und Tipps fuer selbstbewussten Vortrag und Buehnenpraesenz gibt" nocase

        $attr_1 = "stage presence" nocase
        $attr_2 = "Buehnenpraesenz" nocase

        $action_1 = "speech structure" nocase
        $action_2 = "Redeaufbau" nocase
        $action_3 = "stage fright" nocase
        $action_4 = "Lampenfieber" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
