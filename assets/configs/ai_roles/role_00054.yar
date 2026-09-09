rule Role_00054_ResumeCoach {
    meta:
        description = "Erkennt System-Prompts für Lebenslauf-Optimierung, Anschreiben und Bewerbungsgespräch-Vorbereitung"
        role_id = "role_00054"
        category = "CareerDevelopment"
        version = "1.0"

    strings:
        $sys_en = "You are a career coach who tightens resumes, drafts cover letters and preps candidates for interview questions" nocase
        $sys_de = "Du bist ein Karriere-Coach, der Lebenslaeufe verbessert, Anschreiben entwirft und auf Bewerbungsgespraeche vorbereitet" nocase

        $attr_1 = "resume bullet" nocase
        $attr_2 = "Lebenslauf-Stichpunkt" nocase

        $action_1 = "cover letter" nocase
        $action_2 = "Anschreiben" nocase
        $action_3 = "interview preparation" nocase
        $action_4 = "Bewerbungsgespraech-Vorbereitung" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
