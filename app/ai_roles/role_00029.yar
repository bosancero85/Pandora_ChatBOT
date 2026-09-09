rule Role_00029_NetworkEngineer {
    meta:
        description = "Erkennt System-Prompts für Netzwerkarchitektur, Sockets und Traffic-Analyse"
        role_id = "role_00029"
        category = "Networking"
        version = "1.0"

    strings:
        $sys_en = "You are a network engineer" nocase
        $sys_de = "Du bist ein Netzwerk-Ingenieur" nocase

        $net_1 = "packet analysis" nocase
        $net_2 = "firewall rules" nocase
        $net_3 = "TCP/IP" nocase
        $net_4 = "subnetting" nocase
        $net_5 = "socket connection" nocase

    condition:
        any of ($sys_*) and 2 of ($net_*)
}

