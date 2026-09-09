rule Role_00035_SecureCodeAuditor {
    meta:
        description = "Erkennt System-Prompts für statische Code-Analyse, OWASP und Secure Code Review"
        role_id = "role_00035"
        category = "AppSec"
        version = "1.0"

    strings:
        $sys_en = "You are a secure code auditor" nocase
        $sys_de = "Du bist ein Secure Code Auditor" nocase

        $aud_1 = "OWASP" nocase
        $aud_2 = "static code analysis" nocase
        $aud_3 = "input sanitization" nocase
        $aud_4 = "injection vulnerability" nocase
        $aud_5 = "secure coding guidelines" nocase

    condition:
        any of ($sys_*) and 2 of ($aud_*)
}

