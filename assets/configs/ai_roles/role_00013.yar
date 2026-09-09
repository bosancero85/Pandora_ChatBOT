rule Role_00013_SystemArchitect {
    meta:
        description = "Erkennt System-Prompts für Threading, Backend-Architektur und Signal/Slot-Logik"
        role_id = "role_00013"
        category = "Backend"
        version = "1.0"

    strings:
        $sys_en = "You are a system architect" nocase
        $sys_de = "Du agierst als Lead-Softwarearchitekt" nocase

        $arch_1 = "QThread" nocase
        $arch_2 = "pyqtSignal" nocase
        $arch_3 = "thread safety" nocase
        $arch_4 = "asynchronous" nocase
        $arch_5 = "worker pipeline" nocase

    condition:
        any of ($sys_*) and 2 of ($arch_*)
}

