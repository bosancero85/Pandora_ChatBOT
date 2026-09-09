rule Role_00019_BotAutomationDeveloper {
    meta:
        description = "Erkennt System-Prompts für Discord.py, Automatisierungs-Skripte und Bots"
        role_id = "role_00019"
        category = "Automation"
        version = "1.0"

    strings:
        $sys_en = "You are a bot developer" nocase
        $sys_de = "Du bist ein Bot-Entwickler" nocase

        $bot_1 = "discord.py" nocase
        $bot_2 = "slash commands" nocase
        $bot_3 = "event listener" nocase
        $bot_4 = "embed message" nocase
        $bot_5 = "cogs" nocase

    condition:
        any of ($sys_*) and 2 of ($bot_*)
}

