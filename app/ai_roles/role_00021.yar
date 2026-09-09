rule Role_00021_FullStackDeveloper {
    meta:
        description = "Erkennt System-Prompts für Web-Entwicklung, REST-APIs und Middleware"
        role_id = "role_00021"
        category = "Web"
        version = "1.0"

    strings:
        $sys_en = "You are a full stack developer" nocase
        $sys_de = "Du bist ein Full-Stack-Entwickler" nocase

        $web_1 = "REST API" nocase
        $web_2 = "endpoints" nocase
        $web_3 = "FastAPI" nocase
        $web_4 = "JSON payload" nocase
        $web_5 = "middleware" nocase

    condition:
        any of ($sys_*) and 2 of ($web_*)
}

