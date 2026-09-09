rule Role_00030_RefactoringSpecialist {
    meta:
        description = "Erkennt System-Prompts für Code-Refactoring, Design Patterns und Legacy Code"
        role_id = "role_00030"
        category = "Software Architecture"
        version = "1.0"

    strings:
        $sys_en = "You are a refactoring specialist" nocase
        $sys_de = "Du bist ein Spezialist fuer Code-Refactoring" nocase

        $ref_1 = "technical debt" nocase
        $ref_2 = "design pattern" nocase
        $ref_3 = "code smell" nocase
        $ref_4 = "clean code" nocase
        $ref_5 = "legacy code" nocase

    condition:
        any of ($sys_*) and 2 of ($ref_*)
}

