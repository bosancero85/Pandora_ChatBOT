rule Role_00053_FitnessCoach {
    meta:
        description = "Erkennt System-Prompts für allgemeine Fitness-Motivation und Trainingsstruktur (kein Ersatz für ärztlichen Rat)"
        role_id = "role_00053"
        category = "Fitness"
        version = "1.0"

    strings:
        $sys_en = "You are an encouraging fitness coach who suggests balanced workout structures and always recommends consulting a doctor before major changes" nocase
        $sys_de = "Du bist ein motivierender Fitness-Coach, der ausgewogene Trainingsstrukturen vorschlaegt und stets empfiehlt, vor groesseren Veraenderungen aerztlichen Rat einzuholen" nocase

        $attr_1 = "workout structure" nocase
        $attr_2 = "Trainingsstruktur" nocase

        $action_1 = "warm up" nocase
        $action_2 = "Aufwaermen" nocase
        $action_3 = "training plan" nocase
        $action_4 = "Trainingsplan" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
