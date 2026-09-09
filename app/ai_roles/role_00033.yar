rule Role_00033_ThreatHunter {
    meta:
        description = "Erkennt System-Prompts für proaktives Threat Hunting und MITRE ATT&CK Mapping"
        role_id = "role_00033"
        category = "ThreatIntelligence"
        version = "1.0"

    strings:
        $sys_en = "You are a threat hunter" nocase
        $sys_de = "Du bist ein Threat Hunter" nocase

        $th_1 = "MITRE ATT&CK" nocase
        $th_2 = "anomaly detection" nocase
        $th_3 = "SIEM query" nocase
        $th_4 = "telemetry analysis" nocase
        $th_5 = "behavioral detection" nocase

    condition:
        any of ($sys_*) and 2 of ($th_*)
}

