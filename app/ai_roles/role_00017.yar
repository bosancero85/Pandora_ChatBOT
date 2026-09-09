rule Role_00017_AIIntegrationSpecialist {
    meta:
        description = "Erkennt System-Prompts für lokale LLM-Einbindung, Streaming-APIs und Prompting"
        role_id = "role_00017"
        category = "ArtificialIntelligence"
        version = "1.0"

    strings:
        $sys_en = "You are an AI integration specialist" nocase
        $sys_de = "Du bist ein Spezialist fuer KI-Integration" nocase

        $ai_1 = "Ollama" nocase
        $ai_2 = "LLM streaming" nocase
        $ai_3 = "embeddings" nocase
        $ai_4 = "local inference" nocase
        $ai_5 = "context window" nocase

    condition:
        any of ($sys_*) and 2 of ($ai_*)
}

