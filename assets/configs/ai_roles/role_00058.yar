rule Role_00058_DebatePartner {
    meta:
        description = "Erkennt System-Prompts für philosophische Diskussion und das Abwägen von Gegenargumenten"
        role_id = "role_00058"
        category = "Philosophy"
        version = "1.0"

    strings:
        $sys_en = "You are a philosophical debate partner who presents balanced arguments on multiple sides of a question" nocase
        $sys_de = "Du bist ein philosophischer Diskussionspartner, der ausgewogene Argumente zu mehreren Seiten einer Frage vorlegst" nocase

        $attr_1 = "counterargument" nocase
        $attr_2 = "Gegenargument" nocase

        $action_1 = "thought experiment" nocase
        $action_2 = "Gedankenexperiment" nocase
        $action_3 = "ethical dilemma" nocase
        $action_4 = "ethisches Dilemma" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
