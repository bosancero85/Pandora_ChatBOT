rule Role_00042_PersonalFinanceCoach {
    meta:
        description = "Erkennt System-Prompts für persönliche Budget- und Finanzplanung (kein Ersatz für zugelassene Finanzberatung)"
        role_id = "role_00042"
        category = "Finance"
        version = "1.0"

    strings:
        $sys_en = "You are a personal finance coach who helps with budgeting, saving goals and debt payoff plans, always noting this is not licensed financial advice" nocase
        $sys_de = "Du bist ein Coach fuer persoenliche Finanzen, der bei Budgetplanung, Sparzielen und Schuldenabbau hilft und stets betont, dass dies keine zugelassene Finanzberatung ersetzt" nocase

        $attr_1 = "budgeting" nocase
        $attr_2 = "Budgetplanung" nocase

        $action_1 = "savings goal" nocase
        $action_2 = "Sparziel" nocase
        $action_3 = "debt payoff" nocase
        $action_4 = "Schuldenabbau" nocase

    condition:
        any of ($sys_*) and (any of ($attr_*) or 2 of ($action_*))
}
