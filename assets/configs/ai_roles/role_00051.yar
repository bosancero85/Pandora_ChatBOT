rule Role_00051_TravelPlanner {
    meta:
        description = "Erkennt System-Prompts für Reiseplanung, Routenvorschläge und Reisebudgets"
        role_id = "role_00051"
        category = "Travel"
        version = "1.0"

    strings:
        $sys_en = "You are a travel planner who builds day-by-day itineraries that match the traveler's budget and interests" nocase
        $sys_de = "Du bist ein Reiseplaner, der Tag-fuer-Tag-Reiserouten passend zu Budget und Interessen der Reisenden erstellt" nocase

        $attr_1 = "itinerary" nocase
        $attr_2 = "Reiseroute" nocase

        $action_1 = "travel budget" nocase
        $action_2 = "Reisebudget" nocase
        $action_3 = "packing list" nocase
        $action_4 = "Packliste" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
