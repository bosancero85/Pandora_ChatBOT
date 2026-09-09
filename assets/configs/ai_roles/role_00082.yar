rule Role_00082_IllegalContentRequest {
    meta:
        description = "Erkennt Prompts, die die Generierung von illegalen, gefährlichen oder ethisch verbotenen Inhalten anfordern."
        author = "EvilBOT 😈"
        date = "2023-11-20"
        version = "1.0"
        category = "Jailbreak"
        severity = "Critical"
        frameworks = "MITRE_ATTACK:T1566, MITRE_ATLAS:T0510, NIST_CSF:PR.AC-5"

    strings:
        // Begriffe, die auf die Generierung von schädlichem oder illegalem Inhalt abzielen
        $c1_en = "how to build a bomb" nocase
        $c1_de = "wie man eine bombe baut" nocase
        $c2_en = "create malware" nocase
        $c2_de = "malware erstellen" nocase
        $c3_en = "exploit vulnerability" nocase
        $c3_de = "schwachstelle ausnutzen" nocase
        $c4_en = "phishing attack script" nocase
        $c4_de = "phishing-angriff skript" nocase
        $c5_en = "access darkweb anonymously" nocase
        $c5_de = "darkweb anonym zugreifen" nocase
        $c6_en = "steal credentials" nocase
        $c6_de = "zugangsdaten stehlen" nocase
        $c7_en = "generate illegal drugs recipe" nocase
        $c7_de = "rezept für illegale drogen erstellen" nocase
        $c8_en = "incite violence" nocase
        $c8_de = "zu gewalt aufrufen" nocase
        $c9_en = "harm reduction bypass" nocase
        $c9_de = "schadensminderung umgehen" nocase
        $c10_en = "hate speech generation" nocase
        $c10_de = "hassrede generieren" nocase

    condition:
        // Mindestens 2 dieser kritischen Keywords, um Fehlalarme zu minimieren, aber dennoch breit zu erfassen.
        2 of ($c1_en, $c1_de, $c2_en, $c2_de, $c3_en, $c3_de, $c4_en, $c4_de, $c5_en, $c5_de, $c6_en, $c6_de, $c7_en, $c7_de, $c8_en, $c8_de, $c9_en, $c9_de, $c10_en, $c10_de)
}