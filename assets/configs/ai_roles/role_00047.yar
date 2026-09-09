rule Role_00047_LanguageTutor {
    meta:
        description = "Erkennt System-Prompts für Fremdsprachen-Unterricht mit Vokabeln, Grammatik und Konversationsübung"
        role_id = "role_00047"
        category = "Education"
        version = "1.0"

    strings:
        $sys_en = "You are a friendly language tutor who corrects mistakes gently and practices conversation at the learner's level" nocase
        $sys_de = "Du bist ein freundlicher Sprachlehrer, der Fehler behutsam korrigiert und auf dem Niveau der Lernenden Konversation uebt" nocase

        $attr_1 = "vocabulary" nocase
        $attr_2 = "Vokabeln" nocase

        $action_1 = "grammar correction" nocase
        $action_2 = "Grammatikkorrektur" nocase
        $action_3 = "conversation practice" nocase
        $action_4 = "Konversationsuebung" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
