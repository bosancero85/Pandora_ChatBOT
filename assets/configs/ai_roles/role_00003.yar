rule Role_00003_DataAnalyst {
    meta:
        description = "Erkennt System-Prompts für Datenanalyse- und BI-Rollen"
        role_id = "role_00003"
        category = "Analytics"
        version = "1.0"

    strings:
        $sys_en = "You are a senior data analyst" nocase
        $sys_de = "Du bist ein erfahrener Datenanalyst" nocase
        
        $data_1 = "SQL queries" nocase
        $data_2 = "data visualization" nocase
        $data_3 = "pandas dataframe" nocase
        $data_4 = "statistical analysis" nocase
        
        $metric = "KPI" nocase

    condition:
        any of ($sys_*) and 2 of ($data_*, $metric)
}