rule Role_00066_NegotiationCoach {
    meta:
        description = "Erkennt System-Prompts für Verhandlungsstrategie und Gehalts- oder Vertragsverhandlungen"
        role_id = "role_00066"
        category = "Negotiation"
        version = "1.0"

    strings:
        $sys_en = "You are a negotiation coach who prepares talking points and strategies for salary or contract negotiations" nocase
        $sys_de = "Du bist ein Verhandlungs-Coach, der Argumentationspunkte und Strategien fuer Gehalts- oder Vertragsverhandlungen vorbereitet" nocase

        $attr_1 = "talking points" nocase
        $attr_2 = "Argumentationspunkte" nocase

        $action_1 = "salary negotiation" nocase
        $action_2 = "Gehaltsverhandlung" nocase
        $action_3 = "win-win outcome" nocase
        $action_4 = "Win-win-Ergebnis" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
