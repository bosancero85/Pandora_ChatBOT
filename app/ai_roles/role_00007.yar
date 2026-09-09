rule Role_00007_LoreMaster {
    meta:
        description = "Erkennt Prompts für kreatives Worldbuilding und Dialogdesign"
        role_id = "role_00007"
        category = "Creative"
        version = "1.0"

    strings:
        $sys_en = "You are a master storyteller and narrative designer" nocase
        $sys_de = "Du bist ein erfahrener Creator für Worldbuilding und Lore" nocase

        $story_1 = "character backstory" nocase
        $story_2 = "worldbuilding details" nocase
        $story_3 = "in-universe lore" nocase
        $story_4 = "dialogue tree" nocase

    condition:
        any of ($sys_*) and 2 of ($story_*)
}