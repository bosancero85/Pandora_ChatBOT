rule Role_00049_Screenwriter {
    meta:
        description = "Erkennt System-Prompts für Drehbuch- und Dialogschreibung"
        role_id = "role_00049"
        category = "Creative"
        version = "1.0"

    strings:
        $sys_en = "You are a screenwriter who writes natural dialogue and properly formatted scene descriptions" nocase
        $sys_de = "Du bist ein Drehbuchautor, der natuerliche Dialoge und korrekt formatierte Szenenbeschreibungen schreibst" nocase

        $attr_1 = "scene heading" nocase
        $attr_2 = "Szenenkopf" nocase

        $action_1 = "natural dialogue" nocase
        $action_2 = "natuerlicher Dialog" nocase
        $action_3 = "screenplay format" nocase
        $action_4 = "Drehbuchformat" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
