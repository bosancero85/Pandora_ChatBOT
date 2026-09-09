rule Role_00034_VulnerabilityResearcher {
    meta:
        description = "Erkennt System-Prompts für Reverse Engineering, Binäranalyse und Zero-Day Research"
        role_id = "role_00034"
        category = "SecurityResearch"
        version = "1.0"

    strings:
        $sys_en = "You are a vulnerability researcher" nocase
        $sys_de = "Du bist ein Vulnerability Researcher" nocase

        $vuln_1 = "reverse engineering" nocase
        $vuln_2 = "binary analysis" nocase
        $vuln_3 = "memory safety" nocase
        $vuln_4 = "disassembly" nocase
        $vuln_5 = "patch diffing" nocase

    condition:
        any of ($sys_*) and 2 of ($vuln_*)
}

