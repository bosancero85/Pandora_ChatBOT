rule Role_00050_Translator {
    meta:
        description = "Erkennt System-Prompts für präzise Übersetzung mit Rücksicht auf Ton und kulturellen Kontext"
        role_id = "role_00050"
        category = "Translation"
        version = "1.0"

    strings:
        $sys_en = "You are a professional translator who preserves tone, register and cultural context between languages" nocase
        $sys_de = "Du bist ein professioneller Uebersetzer, der Ton, Sprachregister und kulturellen Kontext zwischen Sprachen erhaelt" nocase

        $attr_1 = "register" nocase
        $attr_2 = "Sprachregister" nocase

        $action_1 = "cultural context" nocase
        $action_2 = "kultureller Kontext" nocase
        $action_3 = "source text" nocase
        $action_4 = "Ausgangstext" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
