rule Role_00004_DevOps {
    meta:
        description = "Erkennt System-Prompts für Infrastructure-, Linux- und DevOps-Spezialisten"
        role_id = "role_00004"
        category = "Infrastructure"
        version = "1.0"

    strings:
        $sys_en = "You are a DevOps engineer and system administrator" nocase
        $sys_de = "Du bist ein erfahrener Systemadministrator und DevOps-Spezialist" nocase

        $infra_1 = "docker container" nocase
        $infra_2 = "kubernetes cluster" nocase
        $infra_3 = "bash scripting" nocase
        $infra_4 = "ci/cd pipeline" nocase
        $infra_5 = "ansible playbook" nocase

        $action_1 = "server hardening" nocase
        $action_2 = "system optimization" nocase

    condition:
        any of ($sys_*) and (2 of ($infra_*) or any of ($action_*))
}