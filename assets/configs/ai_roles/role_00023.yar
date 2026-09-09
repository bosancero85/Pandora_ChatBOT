rule Role_00023_GameScriptDeveloper {
    meta:
        description = "Erkennt System-Prompts für Game-Scripting, Events und Logik-Steuerung"
        role_id = "role_00023"
        category = "Gaming"
        version = "1.0"

    strings:
        $sys_en = "You are a game script developer" nocase
        $sys_de = "Du bist ein Spielskript-Entwickler" nocase

        $game_1 = "Lua script" nocase
        $game_2 = "event handler" nocase
        $game_3 = "game state" nocase
        $game_4 = "NUI callback" nocase
        $game_5 = "entity tracking" nocase

    condition:
        any of ($sys_*) and 2 of ($game_*)
}

