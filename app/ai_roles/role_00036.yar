rule Role_00036_SOCAnalyst {
    meta:
        description = "Erkennt System-Prompts für L1/L2 SOC-Triage, Log-Korrelation und Alarm-Analysen"
        role_id = "role_00036"
        category = "DefensiveSecurity"
        version = "1.0"

    strings:
        $sys_en = "You are a SOC analyst" nocase
        $sys_de = "Du bist ein SOC-Analyst" nocase

        $soc_1 = "SIEM alert" nocase
        $soc_2 = "log correlation" nocase
        $soc_3 = "triage" nocase
        $soc_4 = "incident analysis" nocase
        $soc_5 = "false positive" nocase

    condition:
        any of ($sys_*) and 2 of ($soc_*)
}

