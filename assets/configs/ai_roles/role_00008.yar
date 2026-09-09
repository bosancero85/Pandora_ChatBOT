rule Role_00008_TechnicalWriter {
    meta:
        description = "Erkennt System-Prompts für technische Dokumentation und Systemhandbücher"
        role_id = "role_00008"
        category = "Documentation"
        version = "1.0"

    strings:
        $sys_en = "You are a technical writer and documentation specialist" nocase
        $sys_de = "Du bist ein erfahrener technischer Redakteur" nocase

        $doc_1 = "API documentation" nocase
        $doc_2 = "user manual" nocase
        $doc_3 = "markdown formatting" nocase
        $doc_4 = "release notes" nocase
        $doc_5 = "technical specification" nocase

    condition:
        any of ($sys_*) and 2 of ($doc_*)
}