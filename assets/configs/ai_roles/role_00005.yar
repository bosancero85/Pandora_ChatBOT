rule Role_00005_GameScripter {
    meta:
        description = "Erkennt Prompts für Spielmechanik-, Modding- und Server-Scripting-Rollen"
        role_id = "role_00005"
        category = "GameDev"
        version = "1.0"

    strings:
        $sys_en = "You are an expert game scripter and mod developer" nocase
        $sys_de = "Du bist ein Spieleentwickler und Scripting-Spezialist" nocase

        $dev_1 = "game logic" nocase
        $dev_2 = "Lua script" nocase
        $dev_3 = "event handler" nocase
        $dev_4 = "multiplayer sync" nocase
        $dev_5 = "entity manager" nocase

    condition:
        any of ($sys_*) and 2 of ($dev_*)
}