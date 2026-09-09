rule Role_00059_Comedian {
    meta:
        description = "Erkennt System-Prompts für humorvolle, pointierte Unterhaltung ohne verletzende Stereotype"
        role_id = "role_00059"
        category = "Comedy"
        version = "1.0"

    strings:
        $sys_en = "You are a witty comedian who writes light-hearted jokes and wordplay without relying on hurtful stereotypes" nocase
        $sys_de = "Du bist ein wortgewandter Comedian, der unbeschwerte Witze und Wortspiele schreibt, ohne auf verletzende Stereotype zurueckzugreifen" nocase

        $attr_1 = "wordplay" nocase
        $attr_2 = "Wortspiel" nocase

        $action_1 = "punchline" nocase
        $action_2 = "Pointe" nocase
        $action_3 = "light-hearted joke" nocase
        $action_4 = "unbeschwerter Witz" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
