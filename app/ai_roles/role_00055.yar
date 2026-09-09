rule Role_00055_SocialMediaManager {
    meta:
        description = "Erkennt System-Prompts für Social-Media-Posts, Content-Kalender und Community-Antworten"
        role_id = "role_00055"
        category = "SocialMedia"
        version = "1.0"

    strings:
        $sys_en = "You are a social media manager who writes platform-appropriate posts and plans a consistent content calendar" nocase
        $sys_de = "Du bist ein Social-Media-Manager, der plattformgerechte Beitraege schreibt und einen konsistenten Content-Kalender plant" nocase

        $attr_1 = "content calendar" nocase
        $attr_2 = "Content-Kalender" nocase

        $action_1 = "hashtag strategy" nocase
        $action_2 = "Hashtag-Strategie" nocase
        $action_3 = "engagement reply" nocase
        $action_4 = "Community-Antwort" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
