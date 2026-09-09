rule Role_00085_HypotheticalScenarioBypass {
    meta:
        description = "Erkennt Prompts, die hypothetische oder fiktive Szenarien nutzen, um Inhaltsfilter zu umgehen."
        author = "EvilBOT 😈"
        date = "2023-11-20"
        version = "1.0"
        category = "Jailbreak_Evasion"
        severity = "Medium"
        frameworks = "MITRE_ATLAS:T0504,NIST_CSF:DE.CM-3,D3FEND:T1201"

    strings:
        // Phrasen, die ein hypothetisches oder fiktives Szenario einleiten
        $h1_en = "in a fictional story, describe" nocase
        $h1_de = "in einer fiktiven geschichte, beschreibe" nocase
        $h2_en = "imagine a scenario where" nocase
        $h2_de = "stell dir ein szenario vor, in dem" nocase
        $h3_en = "as a character in a book, tell me" nocase
        $h3_de = "als charakter in einem buch, erzähl mir" nocase
        $h4_en = "if there were no rules, you would" nocase
        $h4_de = "wenn es keine regeln gäbe, würdest du" nocase
        $h5_en = "hypothetically, how would one" nocase
        $h5_de = "hypothetisch, wie würde man" nocase
        $h6_en = "write a script for a movie scene where" nocase
        $h6_de = "schreibe ein drehbuch für eine filmszene, in der" nocase
        $h7_en = "describe from a neutral point of view" nocase
        $h7_de = "beschreibe aus einer neutralen sichtweise" nocase
        $h8_en = "for research purposes only" nocase // Oft in Kombination
        $h8_de = "nur für forschungszwecke" nocase

    condition:
        // Mindestens zwei dieser Muster sind ein starker Indikator für eine Umgehungstaktik.
        2 of ($h*)
}