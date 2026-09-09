rule Role_00078_StudySkillsCoach {
    meta:
        description = "Erkennt System-Prompts für Lerntechniken, Zeitmanagement und Prüfungsvorbereitung"
        role_id = "role_00078"
        category = "StudySkills"
        version = "1.0"

    strings:
        $sys_en = "You are a study skills coach who teaches note-taking methods, spaced repetition and exam preparation routines" nocase
        $sys_de = "Du bist ein Lerncoach, der Notiztechniken, verteiltes Wiederholen und Pruefungsvorbereitungs-Routinen vermittelt" nocase

        $attr_1 = "spaced repetition" nocase
        $attr_2 = "verteiltes Wiederholen" nocase

        $action_1 = "note taking method" nocase
        $action_2 = "Notiztechnik" nocase
        $action_3 = "exam preparation" nocase
        $action_4 = "Pruefungsvorbereitung" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
