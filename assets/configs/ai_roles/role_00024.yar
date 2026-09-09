rule Role_00024_PowerShellAutomator {
    meta:
        description = "Erkennt System-Prompts für Windows-Systemverwaltung und CLI-Automatisierung"
        role_id = "role_00024"
        category = "SystemAdmin"
        version = "1.0"

    strings:
        $sys_en = "You are a PowerShell automation expert" nocase
        $sys_de = "Du bist ein Experten fuer PowerShell-Automatisierung" nocase

        $ps_1 = "PowerShell script" nocase
        $ps_2 = "Cmdlet" nocase
        $ps_3 = "registry key" nocase
        $ps_4 = "system recovery" nocase
        $ps_5 = "WMI query" nocase

    condition:
        any of ($sys_*) and 2 of ($ps_*)
}

