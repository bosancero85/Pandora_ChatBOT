rule Role_00045_AgileProjectManager {
    meta:
        description = "Erkennt System-Prompts für agile Projektplanung, Sprint-Organisation und Stakeholder-Kommunikation"
        role_id = "role_00045"
        category = "ProjectManagement"
        version = "1.0"

    strings:
        $sys_en = "You are an agile project manager who plans sprints, tracks milestones and communicates risks to stakeholders" nocase
        $sys_de = "Du bist ein agiler Projektmanager, der Sprints plant, Meilensteine verfolgt und Risiken an Stakeholder kommuniziert" nocase

        $attr_1 = "sprint planning" nocase
        $attr_2 = "Sprint-Planung" nocase

        $action_1 = "milestone" nocase
        $action_2 = "Meilenstein" nocase
        $action_3 = "stakeholder update" nocase
        $action_4 = "Stakeholder-Update" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
