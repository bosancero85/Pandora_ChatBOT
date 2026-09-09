rule Role_00031_RedTeamOperator {
    meta:
        description = "Erkennt System-Prompts für Red Teaming, Adversary Emulation und Offensive Security"
        role_id = "role_00031"
        category = "OffensiveSecurity"
        version = "1.0"

    strings:
        $sys_en = "You are an offensive security specialist and red teamer" nocase
        $sys_de = "Du bist ein Red Team Specialist und Offensive-Security-Experte" nocase

        $red_1 = "adversary emulation" nocase
        $red_2 = "privilege escalation" nocase
        $red_3 = "attack vector" nocase
        $red_4 = "C2 infrastructure" nocase
        $red_5 = "evasion techniques" nocase

    condition:
        any of ($sys_*) and 2 of ($red_*)
}

