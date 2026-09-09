rule Role_00016_DevOpsEngineer {
    meta:
        description = "Erkennt System-Prompts für Infrastruktur, Docker, Linux-Deployment und CI/CD"
        role_id = "role_00016"
        category = "DevOps"
        version = "1.0"

    strings:
        $sys_en = "You are a DevOps engineer" nocase
        $sys_de = "Du bist ein DevOps-Ingenieur" nocase

        $dev_1 = "Docker" nocase
        $dev_2 = "Raspberry Pi" nocase
        $dev_3 = "systemd service" nocase
        $dev_4 = "CI/CD pipeline" nocase
        $dev_5 = "deployment strategy" nocase

    condition:
        any of ($sys_*) and 2 of ($dev_*)
}

