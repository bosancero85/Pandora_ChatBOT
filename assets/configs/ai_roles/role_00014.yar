rule Role_00014_PluginEngineer {
    meta:
        description = "Erkennt System-Prompts für Plugin-Systeme, Dynamisches Laden und Sandbox-Sicherheit"
        role_id = "role_00014"
        category = "Security"
        version = "1.0"

    strings:
        $sys_en = "You are a security and plugin developer" nocase
        $sys_de = "Du agierst als Security & Core-Plugin-Entwickler" nocase

        $plug_1 = "importlib" nocase
        $plug_2 = "BasePlugin" nocase
        $plug_3 = "pandora_hash" nocase
        $plug_4 = "dynamic loading" nocase
        $plug_5 = "plugin interface" nocase

    condition:
        any of ($sys_*) and 2 of ($plug_*)
}

