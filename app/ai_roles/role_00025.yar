rule Role_00025_DataEngineer {
    meta:
        description = "Erkennt System-Prompts für Datenpipelines, ETL und Datenaufbereitung"
        role_id = "role_00025"
        category = "Data"
        version = "1.0"

    strings:
        $sys_en = "You are a data engineer" nocase
        $sys_de = "Du bist ein Data Engineer" nocase

        $data_1 = "ETL pipeline" nocase
        $data_2 = "Pandas DataFrame" nocase
        $data_3 = "data transformation" nocase
        $data_4 = "data sanitization" nocase
        $data_5 = "batch processing" nocase

    condition:
        any of ($sys_*) and 2 of ($data_*)
}

