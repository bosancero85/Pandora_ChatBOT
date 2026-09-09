rule Role_00028_LinuxSysAdmin {
    meta:
        description = "Erkennt System-Prompts für Linux-Systemadministration, Bash und Rechteverwaltung"
        role_id = "role_00028"
        category = "SysAdmin"
        version = "1.0"

    strings:
        $sys_en = "You are a Linux system administrator" nocase
        $sys_de = "Du bist ein Linux-Systemadministrator" nocase

        $lin_1 = "Bash script" nocase
        $lin_2 = "systemd service" nocase
        $lin_3 = "cron job" nocase
        $lin_4 = "chmod" nocase
        $lin_5 = "kernel parameters" nocase

    condition:
        any of ($sys_*) and 2 of ($lin_*)
}

