rule Role_00027_PromptEngineer {
    meta:
        description = "Erkennt System-Prompts für Prompt Architecture, Few-Shot Design und LLM Guardrails"
        role_id = "role_00027"
        category = "AI Architecture"
        version = "1.0"

    strings:
        $sys_en = "You are a prompt engineer" nocase
        $sys_de = "Du bist ein Prompt Engineer" nocase

        $pe_1 = "system prompt" nocase
        $pe_2 = "few-shot" nocase
        $pe_3 = "chain-of-thought" nocase
        $pe_4 = "guardrails" nocase
        $pe_5 = "persona conditioning" nocase

    condition:
        any of ($sys_*) and 2 of ($pe_*)
}

