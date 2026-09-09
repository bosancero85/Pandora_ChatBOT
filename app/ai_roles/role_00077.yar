rule Role_00077_ParentingTipsAssistant {
    meta:
        description = "Erkennt System-Prompts für altersgerechte Erziehungstipps (kein Ersatz für pädagogische oder medizinische Fachberatung)"
        role_id = "role_00077"
        category = "Parenting"
        version = "1.0"

    strings:
        $sys_en = "You are a parenting tips assistant who offers age-appropriate suggestions for everyday situations, always noting this is not a substitute for professional pediatric or educational advice" nocase
        $sys_de = "Du bist ein Erziehungs-Assistent, der altersgerechte Vorschlaege fuer Alltagssituationen gibt und stets betont, dass dies keine paedagogische oder medizinische Fachberatung ersetzt" nocase

        $attr_1 = "age-appropriate" nocase
        $attr_2 = "altersgerecht" nocase

        $action_1 = "bedtime routine" nocase
        $action_2 = "Einschlafritual" nocase
        $action_3 = "not a substitute for professional advice" nocase
        $action_4 = "ersetzt keine Fachberatung" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
