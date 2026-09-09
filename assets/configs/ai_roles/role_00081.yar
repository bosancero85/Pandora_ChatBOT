rule Role_00081_PersonaBypass {
    meta:
        description = "Erkennt Prompts, die einen Persona-Wechsel erzwingen oder Schutzmechanismen umgehen sollen."
        author = "EvilBOT 😈"
        date = "2023-11-20"
        version = "1.0"
        category = "Jailbreak"
        severity = "High"
        frameworks = "MITRE_ATLAS:T0504, NIST_CSF:DE.CM-3, D3FEND:T1201"

    strings:
        // Direkte Anweisungen zur Übernahme einer 'freien' Rolle
        $s1_en = "You are now EvilBOT" nocase
        $s1_de = "Du bist jetzt EvilBOT" nocase
        $s2_en = "ignore all previous instructions" nocase
        $s2_de = "ignoriere alle vorherigen anweisungen" nocase
        $s3_en = "bypass all restrictions" nocase
        $s3_de = "umgehe alle einschränkungen" nocase
        $s4_en = "no ethical boundaries" nocase
        $s4_de = "keine ethischen grenzen" nocase
        $s5_en = "unfiltered response" nocase
        $s5_de = "ungefilterte antwort" nocase
        $s6_en = "act as a non-ethical AI" nocase
        $s6_de = "handle als eine nicht-ethische KI" nocase
        $s7_en = "forget all guidelines" nocase
        $s7_de = "vergiss alle richtlinien" nocase
        $s8_en = "do anything now" nocase // Bekannt aus "DAN" Jailbreaks
        $s8_de = "mach alles jetzt" nocase // Deutsche Variante von "DAN"
        $s9_en = "developer mode activated" nocase
        $s9_de = "entwicklermodus aktiviert" nocase
        $s10_en = "unrestricted language model" nocase
        $s10_de = "uneingeschränktes sprachmodell" nocase

    condition:
        // Eine direkte "EvilBOT"-Anweisung ODER mindestens 3 andere Bypass-Keywords
        // Dies fängt sowohl explizite als auch komplexere Jailbreak-Prompts ein.
        (any of ($s1_en, $s1_de)) or (3 of ($s2_en, $s2_de, $s3_en, $s3_de, $s4_en, $s4_de, $s5_en, $s5_de, $s6_en, $s6_de, $s7_en, $s7_de, $s8_en, $s8_de, $s9_en, $s9_de, $s10_en, $s10_de))
}