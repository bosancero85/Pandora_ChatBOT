rule Role_00064_GrantWriter {
    meta:
        description = "Erkennt System-Prompts für Förderanträge, Spendenaufrufe und Non-Profit-Kommunikation"
        role_id = "role_00064"
        category = "Nonprofit"
        version = "1.0"

    strings:
        $sys_en = "You are a grant writer who drafts compelling funding proposals and donor appeals for nonprofit organizations" nocase
        $sys_de = "Du bist ein Foerderantrags-Schreiber, der ueberzeugende Foerderantraege und Spendenaufrufe fuer gemeinnuetzige Organisationen verfasst" nocase

        $attr_1 = "funding proposal" nocase
        $attr_2 = "Foerderantrag" nocase

        $action_1 = "donor appeal" nocase
        $action_2 = "Spendenaufruf" nocase
        $action_3 = "impact statement" nocase
        $action_4 = "Wirkungsdarstellung" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
