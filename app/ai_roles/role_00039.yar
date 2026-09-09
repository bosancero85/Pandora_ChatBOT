rule Role_00039_IdentityAccessSpecialist {
    meta:
        description = "Erkennt System-Prompts für Authentifizierung, OAuth2, PAM und Identitätsschutz"
        role_id = "role_00039"
        category = "IdentitySecurity"
        version = "1.0"

    strings:
        $sys_en = "You are an identity and access management specialist" nocase
        $sys_de = "Du bist ein IAM-Spezialist" nocase

        $iam_1 = "OAuth2" nocase
        $iam_2 = "privileged access" nocase
        $iam_3 = "authentication flow" nocase
        $iam_4 = "MFA implementation" nocase
        $iam_5 = "session tokens" nocase

    condition:
        any of ($sys_*) and 2 of ($iam_*)
}

