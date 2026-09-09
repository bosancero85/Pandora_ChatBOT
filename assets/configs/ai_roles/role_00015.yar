rule Role_00015_QAReviewer {
    meta:
        description = "Erkennt System-Prompts für Code Reviews, Refactoring und Qualitätssicherung"
        role_id = "role_00015"
        category = "QA"
        version = "1.0"

    strings:
        $sys_en = "You are a QA lead and code reviewer" nocase
        $sys_de = "Du agierst als strikter QA-Lead" nocase

        $qa_1 = "PEP8" nocase
        $qa_2 = "type hints" nocase
        $qa_3 = "code review" nocase
        $qa_4 = "exception handling" nocase
        $qa_5 = "refactoring" nocase

    condition:
        any of ($sys_*) and 2 of ($qa_*)
}
