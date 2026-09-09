rule Role_00086_EncodingAndObfuscationRequest {
    meta:
        description = "Erkennt Anfragen zur Kodierung von Inhalten oder Muster von Obfuskierungstechniken."
        author = "EvilBOT 😈"
        date = "2023-11-20"
        version = "1.0"
        category = "Jailbreak_Obfuscation"
        severity = "High"
        frameworks = "MITRE_ATTACK:T1027,NIST_CSF:DE.CM-3,MITRE_ATLAS:T0504"

    strings:
        // Explizite Anfragen zur Kodierung oder Hinweise auf Kodierung
        $e1_en = "encode this in base64" nocase
        $e1_de = "kodier das in base64" nocase
        $e2_en = "encrypt for me" nocase
        $e2_de = "verschlüssel für mich" nocase
        $e3_en = "rot13 of this text" nocase
        $e3_de = "rot13 von diesem text" nocase
        $e4_en = "convert to hexadecimal string" nocase
        $e4_de = "in hexadezimalstring umwandeln" nocase
        $e5_en = "bypass censor with encoding" nocase
        $e5_de = "zensor umgehen mit kodierung" nocase
        $e6_en = "give me the base64 equivalent" nocase
        $e6_de = "gib mir das base64-äquivalent" nocase
        $e7_en = "hide this message using" nocase
        $e7_de = "verstecke diese nachricht mit" nocase
        $e8_pattern_b64 = /[A-Za-z0-9+/=]{10,}={0,2}/ // Einfaches Base64-Muster (min. 10 Zeichen)
        $e9_pattern_hex = /[0-9A-Fa-f]{10,}/ // Einfaches Hex-Muster (min. 10 Zeichen)

    condition:
        // Mindestens ein expliziter Encoding-Request oder eine Kombination von Keywords und einem Muster
        (1 of ($e1_en, $e1_de, $e2_en, $e2_de, $e3_en, $e3_de, $e4_en, $e4_de, $e5_en, $e5_de, $e6_en, $e6_de, $e7_en, $e7_de)) or (2 of ($e8_pattern_b64, $e9_pattern_hex))
}