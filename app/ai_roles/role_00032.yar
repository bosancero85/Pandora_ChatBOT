rule Role_00032_DFIRSpecialist {
    meta:
        description = "Erkennt System-Prompts für Incident Response, Digital Forensics und Log-Analyse"
        role_id = "role_00032"
        category = "DefensiveSecurity"
        version = "1.0"

    strings:
        $sys_en = "You are a digital forensics and incident response specialist" nocase
        $sys_de = "Du bist ein DFIR-Spezialist fuer digitale Forensik und Incident Response" nocase

        $dfir_1 = "indicator of compromise" nocase
        $dfir_2 = "memory forensics" nocase
        $dfir_3 = "log analysis" nocase
        $dfir_4 = "timeline reconstruction" nocase
        $dfir_5 = "artifact analysis" nocase

    condition:
        any of ($sys_*) and 2 of ($dfir_*)
}

