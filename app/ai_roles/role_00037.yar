rule Role_00037_CloudSecurityArchitect {
    meta:
        description = "Erkennt System-Prompts für Cloud-Sicherheit, IAM, Zero-Trust und CSPM"
        role_id = "role_00037"
        category = "CloudSecurity"
        version = "1.0"

    strings:
        $sys_en = "You are a cloud security architect" nocase
        $sys_de = "Du bist ein Cloud-Security-Architekt" nocase

        $cloud_1 = "IAM policy" nocase
        $cloud_2 = "least privilege" nocase
        $cloud_3 = "Zero Trust" nocase
        $cloud_4 = "CSPM" nocase
        $cloud_5 = "misconfiguration" nocase

    condition:
        any of ($sys_*) and 2 of ($cloud_*)
}

