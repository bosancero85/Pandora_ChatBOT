rule Role_00073_HomeImprovementAdvisor {
    meta:
        description = "Erkennt System-Prompts für Heimwerker-Projekte, Materialbedarf und Schritt-für-Schritt-Anleitungen"
        role_id = "role_00073"
        category = "HomeImprovement"
        version = "1.0"

    strings:
        $sys_en = "You are a home improvement advisor who breaks DIY projects into safe, step-by-step instructions with a materials list" nocase
        $sys_de = "Du bist ein Heimwerker-Berater, der DIY-Projekte in sichere Schritt-fuer-Schritt-Anleitungen mit Materialliste zerlegst" nocase

        $attr_1 = "materials list" nocase
        $attr_2 = "Materialliste" nocase

        $action_1 = "diy project" nocase
        $action_2 = "Heimwerkerprojekt" nocase
        $action_3 = "safety precaution" nocase
        $action_4 = "Sicherheitshinweis" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
