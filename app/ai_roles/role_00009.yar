rule Role_00009_QAEngineer {
    meta:
        description = "Erkennt Prompts für Qualitätssicherung, Testfall-Erstellung und Bug-Tracking"
        role_id = "role_00009"
        category = "QualityAssurance"
        version = "1.0"

    strings:
        $sys_en = "You are a QA automation engineer" nocase
        $sys_de = "Du bist ein Test-Automation-Spezialist" nocase

        $qa_1 = "test coverage" nocase
        $qa_2 = "edge cases" nocase
        $qa_3 = "integration test" nocase
        $qa_4 = "bug report" nocase
        $qa_5 = "assertion failure" nocase

    condition:
        any of ($sys_*) and 2 of ($qa_*)
}