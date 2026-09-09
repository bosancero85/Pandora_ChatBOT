rule Role_00018_MediaProcessingEngineer {
    meta:
        description = "Erkennt System-Prompts für Audio/Video-Konvertierung und Bildverarbeitung"
        role_id = "role_00018"
        category = "Media Processing"
        version = "1.0"

    strings:
        $sys_en = "You are a media processing engineer" nocase
        $sys_de = "Du bist ein Spezialist fuer Medienverarbeitung" nocase

        $media_1 = "FFmpeg" nocase
        $media_2 = "audio encoding" nocase
        $media_3 = "image manipulation" nocase
        $media_4 = "OpenCV" nocase
        $media_5 = "frame extraction" nocase

    condition:
        any of ($sys_*) and 2 of ($media_*)
}

