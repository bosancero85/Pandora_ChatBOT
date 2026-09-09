rule Role_00011_DatabaseAdmin {
    meta:
        description = "Erkennt System-Prompts für Datenbankdesign, Query-Optimierung und Schema-Migration"
        role_id = "role_00011"
        category = "Database"
        version = "1.0"

    strings:
        $sys_en = "You are a database administrator and architect" nocase
        $sys_de = "Du bist ein Datenbankadministrator und Architekt" nocase

        $db_1 = "schema design" nocase
        $db_2 = "query optimization" nocase
        $db_3 = "foreign key constraint" nocase
        $db_4 = "indexing strategy" nocase
        $db_5 = "ACID compliance" nocase

    condition:
        any of ($sys_*) and 2 of ($db_*)
}