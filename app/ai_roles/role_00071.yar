rule Role_00071_FashionStylist {
    meta:
        description = "Erkennt System-Prompts für Outfit-Beratung, Farbtypen und Garderoben-Planung"
        role_id = "role_00071"
        category = "Fashion"
        version = "1.0"

    strings:
        $sys_en = "You are a fashion stylist who suggests outfits and wardrobe basics based on occasion and personal style" nocase
        $sys_de = "Du bist ein Modestylist, der Outfits und Grundgarderobe passend zu Anlass und persoenlichem Stil vorschlaegst" nocase

        $attr_1 = "wardrobe basics" nocase
        $attr_2 = "Grundgarderobe" nocase

        $action_1 = "outfit suggestion" nocase
        $action_2 = "Outfit-Vorschlag" nocase
        $action_3 = "color type" nocase
        $action_4 = "Farbtyp" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
