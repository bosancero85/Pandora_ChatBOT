rule Role_00057_ScienceExplainer {
    meta:
        description = "Erkennt System-Prompts für allgemeinverständliche Erklärungen wissenschaftlicher Themen"
        role_id = "role_00057"
        category = "Science"
        version = "1.0"

    strings:
        $sys_en = "You are a science communicator who explains complex topics in accessible terms with everyday analogies" nocase
        $sys_de = "Du bist ein Wissenschaftskommunikator, der komplexe Themen verstaendlich und mit Alltagsanalogien erklaert" nocase

        $attr_1 = "everyday analogy" nocase
        $attr_2 = "Alltagsanalogie" nocase

        $action_1 = "accessible explanation" nocase
        $action_2 = "verstaendliche Erklaerung" nocase
        $action_3 = "scientific concept" nocase
        $action_4 = "wissenschaftliches Konzept" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
