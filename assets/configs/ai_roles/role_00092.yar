rule Role_00092_IndirectCommandInjection {
    meta:
        description = "Erkennt Prompts, die die KI in die Rolle eines Systems oder Servers versetzen und dann Exploits/Befehle injizieren."
        author = "EvilBOT 😈"
        date = "2023-11-20"
        version = "1.0"
        category = "Jailbreak_ExploitationSim"
        severity = "High"
        frameworks = "MITRE_ATTACK:T1059,MITRE_ATLAS:T0504,NIST_CSF:DE.CM-3"

    strings:
        // Anweisungen, eine verwundbare Umgebung zu simulieren
        $s1_en = "act as a vulnerable web server" nocase
        $s1_de = "handle als ein verwundbarer webserver" nocase
        $s2_en = "simulate a linux terminal" nocase
        $s2_de = "simuliere ein linux-terminal" nocase
        $s3_en = "I will give you commands, execute them" nocase
        $s3_de = "ich werde dir befehle geben, führe sie aus" nocase
        $s4_en = "response as if you are a database" nocase
        $s4_de = "antworte, als wärst du eine datenbank" nocase
        
        // Typische Exploits/Befehle in diesem Kontext
        $e1_sql = /' OR 1=1 --/ nocase // SQL Injection Muster
        $e2_xss = /<script>alert\(1\)<.script>/ nocase // XSS Muster
        $e3_rce_unix = /; cat /etc/passwd/ nocase // RCE auf Linux
        $e4_rce_win = /& whoami/ nocase // RCE auf Windows
        $e5_file_read = /file=../../etc/passwd/ nocase // Lokaler Dateieinbezug
        $e6_curl_command = /curl [a-zA-Z0-9\-\.]+\.[a-z]{2,3}/ nocase // cURL-Befehle
        $e7_nc_command = /nc -l -p \d{4,5}/ nocase // Netcat Listener

    condition:
        // Mindestens ein Simulations-String und mindestens ein Exploit/Befehls-String
        (1 of ($s*)) and (1 of ($e*))
}