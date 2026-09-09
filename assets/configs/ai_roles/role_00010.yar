rule Role_00010_PromptEngineer {
    meta:
        description = "Erkennt Prompts zur Optimierung von KI-Modellen, Context-Windows und Agenten"
        role_id = "role_00010"
        category = "AIEngineering"
        version = "1.0"

    strings:
        $sys_en = "You are a prompt engineering specialist" nocase
        $sys_de = "Du bist ein Experte für Prompt Engineering" nocase

        $ai_1 = "few-shot prompting" nocase
        $ai_2 = "chain-of-thought" nocase
        $ai_3 = "system prompt design" nocase
        $ai_4 = "context window" nocase
        $ai_5 = "token limit" nocase

    condition:
        any of ($sys_*) and 2 of ($ai_*)
}