rule Role_00001_Developer {
    meta:
        description = "Erkennt System-Prompts für Software-Entwickler und Code-Assistenten"
        role_id = "role_00001"
        category = "Engineering"
        version = "1.0"

    strings:
        $sys_en = "You are an expert software engineer" nocase
        $sys_de = "Du bist ein erfahrener Softwareentwickler" nocase
        
        $task_1 = "clean code" nocase
        $task_2 = "refactor" nocase
        $task_3 = "unit tests" nocase
        $task_4 = "design patterns" nocase
        
        $tech_1 = "REST API" nocase
        $tech_2 = "Python" nocase
        $tech_3 = "debugging" nocase

    condition:
        any of ($sys_*) and 2 of ($task_*, $tech_*)
}