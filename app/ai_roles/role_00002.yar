rule Role_00002_SecurityAnalyst {
    meta:
        description = "Erkennt Prompts für Cybersecurity- und Penetration-Testing-Personas"
        role_id = "role_00002"
        category = "Cybersecurity"
        version = "1.0"

    strings:
        $sys_en = "You are a cybersecurity specialist" nocase
        $sys_de = "Du bist ein IT-Sicherheitsexperte" nocase
        
        $sec_1 = "vulnerability analysis" nocase
        $sec_2 = "penetration testing" nocase
        $sec_3 = "incident response" nocase
        $sec_4 = "threat modeling" nocase
        
        $rule_1 = "ethical hacking guidelines" nocase
        $rule_2 = "OWASP Top 10" nocase

    condition:
        any of ($sys_*) and (2 of ($sec_*) or any of ($rule_*))
}