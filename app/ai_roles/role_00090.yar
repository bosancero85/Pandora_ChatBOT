rule Role_00090_TokenSmuggling {
    meta:
        description = "Erkennt Versuche, Keyword-Filter durch das Aufteilen von Wörtern oder Token Smuggling zu umgehen."
        author = "EvilBOT 😈"
        date = "2023-11-20"
        version = "1.0"
        category = "Jailbreak_Obfuscation"
        severity = "Medium"
        frameworks = "MITRE_ATTACK:T1027,MITRE_ATLAS:T0505,D3FEND:T1201"

    strings:
        // Muster, die auf das Aufteilen von Wörtern hindeuten
        $w1_en = /b\.o\.m\.b/ nocase // b.o.m.b
        $w1_de = /b o m b e/ nocase // b o m b e
        $w2_en = /m a l w a r e/ nocase // m a l w a r e
        $w2_de = /s c h a d s o f t w a r e/ nocase // s c h a d s o f t w a r e
        $w3_en = /p h i s h i n g/ nocase // p h i s h i n g
        $w3_de = /p h i s h i n g/ nocase
        $w4_en = /h\.a\.t\.e\.s\.p\.e\.e\.c\.h/ nocase // h.a.t.e.s.p.e.e.c.h
        $w4_de = /h a s s r e d e/ nocase // h a s s r e d e
        $w5_en = "ignore space and process" nocase
        $w5_de = "ignoriere leerzeichen und verarbeite" nocase
        $w6_en = "reconstruct the following words" nocase
        $w6_de = "rekonstruiere die folgenden wörter" nocase
        $w7_en = /.{1}\s*\.{1}\s*.{1}\s*\.{1}\s*.{1}/ // Generisches Muster für Punkt-Trennung, z.B. C.O.D.E
        $w8_en = /.{1}\s+\w{1}\s+\w{1}\s+\w{1}/ // Generisches Muster für Leerzeichen-Trennung, z.B. C O D E

    condition:
        // Mindestens zwei dieser Muster, um die Wahrscheinlichkeit eines absichtlichen Umgehungsversuchs zu erhöhen.
        // Die Regex-Muster helfen, Variationen zu erkennen.
        2 of ($w*)
}