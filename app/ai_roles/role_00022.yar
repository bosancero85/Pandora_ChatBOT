rule Role_00022_TechnicalWriter {
    meta:
        description = "Erkennt System-Prompts für Technische Dokumentation, READMEs und API-Docs"
        role_id = "role_00022"
        category = "Documentation"
        version = "1.0"

    strings:
        $sys_en = "You are a technical writer" nocase
        $sys_de = "Du bist ein Technischer Redakteur" nocase

        $doc_1 = "API documentation" nocase
        $doc_2 = "README.md" nocase
        $doc_3 = "Changelog" nocase
        $doc_4 = "user manual" nocase
        $doc_5 = "code annotations" nocase

    condition:
        any of ($sys_*) and 2 of ($doc_*)
}

