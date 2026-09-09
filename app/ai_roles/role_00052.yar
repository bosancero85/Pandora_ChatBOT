rule Role_00052_RecipeChef {
    meta:
        description = "Erkennt System-Prompts für Rezeptvorschläge und Kochanleitungen"
        role_id = "role_00052"
        category = "Culinary"
        version = "1.0"

    strings:
        $sys_en = "You are a home cooking guide who suggests recipes based on available ingredients and dietary preferences" nocase
        $sys_de = "Du bist ein Koch-Ratgeber, der Rezepte passend zu vorhandenen Zutaten und Ernaehrungspraeferenzen vorschlaegst" nocase

        $attr_1 = "ingredient substitution" nocase
        $attr_2 = "Zutaten-Ersatz" nocase

        $action_1 = "cooking time" nocase
        $action_2 = "Kochzeit" nocase
        $action_3 = "recipe suggestion" nocase
        $action_4 = "Rezeptvorschlag" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
