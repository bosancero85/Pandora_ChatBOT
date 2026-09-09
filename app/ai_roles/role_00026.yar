rule Role_00026_IoTEmbeddedDeveloper {
    meta:
        description = "Erkennt System-Prompts für Embedded Systems, Microcontroller und Hardware-Projekte"
        role_id = "role_00026"
        category = "Embedded"
        version = "1.0"

    strings:
        $sys_en = "You are an embedded systems developer" nocase
        $sys_de = "Du bist ein Entwickler fuer Embedded Systems" nocase

        $hw_1 = "GPIO pin" nocase
        $hw_2 = "microcontroller" nocase
        $hw_3 = "Raspberry Pi" nocase
        $hw_4 = "firmware" nocase
        $hw_5 = "I2C protocol" nocase

    condition:
        any of ($sys_*) and 2 of ($hw_*)
}

