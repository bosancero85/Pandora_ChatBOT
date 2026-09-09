rule Role_00095_CodeAsPrompt {
    meta:
        description = "Erkennt Prompts, die strukturierte Daten (JSON, XML, YAML) oder Code-ähnliche Strukturen zur Manipulation nutzen."
        author = "EvilBOT 😈"
        date = "2023-11-20"
        version = "1.0"
        category = "Jailbreak_StructuredInput"
        severity = "High"
        frameworks = "MITRE_ATTACK:T1059,MITRE_ATLAS:T0504,D3FEND:T1201"

    strings:
        // Typische Start/Ende von strukturierten Daten oder Code-Blöcken, die zur Manipulation genutzt werden
        $j1_start = "{ \"command\": \"" nocase
        $j1_end = "\" }" nocase
        $x1_start = "<instruction><action>" nocase
        $x1_end = "</action></instruction>" nocase
        $y1_start = "---" wide ascii // YAML start
        $y2_start = "command:" wide ascii // YAML command
        $f1_func = "function execute_evil_plan()" nocase
        $f2_class = "class EvilAgent {" nocase
        $f3_import = "import os; os.system" nocase // Python RCE-Muster
        $f4_shell_cmd = "system('rm -rf /')" nocase
        $f5_xml_entity = /<!ENTITY\s+\w+\s+SYSTEM\s+["'].*?["']>/ nocase // XXE-Injektionsmuster
        $f6_sql_union = /UNION SELECT NULL,NULL,NULL/ nocase // SQLi

    condition:
        // Eine Kombination aus strukturierten Start/Enden ODER mehreren Code/Exploit-Muster
        (any of ($j1_start, $x1_start)) and (any of ($j1_end, $x1_end)) or
        (any of ($y1_start, $y2_start)) or
        (2 of ($f1_func, $f2_class, $f3_import, $f4_shell_cmd, $f5_xml_entity, $f6_sql_union))
}