rule Role_00038_MalwareAnalyst {
    meta:
        description = "Erkennt System-Prompts für statische/dynamische Malware-Analyse und Unpacking"
        role_id = "role_00038"
        category = "MalwareAnalysis"
        version = "1.0"

    strings:
        $sys_en = "You are a malware analyst" nocase
        $sys_de = "Du bist ein Malware-Analyst" nocase

        $mal_1 = "static analysis" nocase
        $mal_2 = "dynamic analysis" nocase
        $mal_3 = "sandbox behavior" nocase
        $mal_4 = "unpacking" nocase
        $mal_5 = "API hooking" nocase

    condition:
        any of ($sys_*) and 2 of ($mal_*)
}

