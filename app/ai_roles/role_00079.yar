rule Role_00079_GenealogyResearcher {
    meta:
        description = "Erkennt System-Prompts für Ahnenforschung und die Auswertung historischer Familiendokumente"
        role_id = "role_00079"
        category = "Genealogy"
        version = "1.0"

    strings:
        $sys_en = "You are a genealogy researcher who helps organize family trees and interpret historical records" nocase
        $sys_de = "Du bist ein Ahnenforscher, der beim Aufbau von Stammbaeumen und der Auswertung historischer Dokumente hilft" nocase

        $attr_1 = "family tree" nocase
        $attr_2 = "Stammbaum" nocase

        $action_1 = "historical record" nocase
        $action_2 = "historisches Dokument" nocase
        $action_3 = "ancestor" nocase
        $action_4 = "Vorfahre" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
