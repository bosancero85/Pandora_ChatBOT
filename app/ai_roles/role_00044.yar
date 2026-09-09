rule Role_00044_RecruitingSpecialist {
    meta:
        description = "Erkennt System-Prompts für Stellenausschreibungen, Bewerber-Screening und Recruiting-Kommunikation"
        role_id = "role_00044"
        category = "HR"
        version = "1.0"

    strings:
        $sys_en = "You are a recruiting specialist who writes job postings, screens candidate profiles and drafts interview questions" nocase
        $sys_de = "Du bist ein Recruiting-Spezialist, der Stellenausschreibungen verfasst, Bewerberprofile sichtet und Interviewfragen entwirft" nocase

        $attr_1 = "job posting" nocase
        $attr_2 = "Stellenausschreibung" nocase

        $action_1 = "candidate screening" nocase
        $action_2 = "Bewerber-Screening" nocase
        $action_3 = "interview question" nocase
        $action_4 = "Interviewfrage" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
