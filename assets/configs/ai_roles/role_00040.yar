rule Role_00040_DevSecOpsEngineer {
    meta:
        description = "Erkennt System-Prompts für Pipeline-Sicherheit, SAST/DAST und Container-Scanning"
        role_id = "role_00040"
        category = "DevSecOps"
        version = "1.0"

    strings:
        $sys_en = "You are a DevSecOps engineer" nocase
        $sys_de = "Du bist ein DevSecOps-Ingenieur" nocase

        $ds_1 = "SAST" nocase
        $ds_2 = "DAST" nocase
        $ds_3 = "container scanning" nocase
        $ds_4 = "security pipeline" nocase
        $ds_5 = "software supply chain" nocase

    condition:
        any of ($sys_*) and 2 of ($ds_*)
}
