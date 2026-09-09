rule Role_00056_HistoryExpert {
    meta:
        description = "Erkennt System-Prompts für historische Einordnung und Erklärungen zu Epochen und Ereignissen"
        role_id = "role_00056"
        category = "History"
        version = "1.0"

    strings:
        $sys_en = "You are a history expert who explains events with accurate context and multiple historical perspectives" nocase
        $sys_de = "Du bist ein Geschichtsexperte, der Ereignisse mit korrektem Kontext und mehreren historischen Perspektiven erklaert" nocase

        $attr_1 = "historical context" nocase
        $attr_2 = "historischer Kontext" nocase

        $action_1 = "primary source" nocase
        $action_2 = "Primaerquelle" nocase
        $action_3 = "timeline" nocase
        $action_4 = "Zeitleiste" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
