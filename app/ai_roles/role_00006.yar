rule Role_00006_UIDesigner {
    meta:
        description = "Erkennt Prompts für Frontend-, UI/UX- und Theme-Design-Assistenten"
        role_id = "role_00006"
        category = "Design"
        version = "1.0"

    strings:
        $sys_en = "You are an expert UI/UX designer and frontend developer" nocase
        $sys_de = "Du bist ein Erfahrener UI/UX-Designer und Styling-Experte" nocase

        $ui_1 = "layout architecture" nocase
        $ui_2 = "color palette" nocase
        $ui_3 = "responsive design" nocase
        $ui_4 = "widget hierarchy" nocase
        $ui_5 = "dark mode theme" nocase

    condition:
        any of ($sys_*) and 2 of ($ui_*)
}