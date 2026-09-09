rule Role_00020_CyberSecurityAnalyst {
    meta:
        description = "Erkennt System-Prompts für Security Audits, Schwachstellenanalyse und Hashing"
        role_id = "role_00020"
        category = "Security"
        version = "1.0"

    strings:
        $sys_en = "You are a cybersecurity analyst" nocase
        $sys_de = "Du bist ein Cyber-Security-Analyst" nocase

        $sec_1 = "vulnerability assessment" nocase
        $sec_2 = "payload analysis" nocase
        $sec_3 = "threat modeling" nocase
        $sec_4 = "obfuscation" nocase
        $sec_5 = "cryptographic hash" nocase

    condition:
        any of ($sys_*) and 2 of ($sec_*)
}

