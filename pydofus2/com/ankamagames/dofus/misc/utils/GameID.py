class GameID:
    # Game ID constants
    DOFUS = 1
    DOFUS_ARENA = 2
    WAKFU = 3
    DOFUS_POCKET = 4
    WAKFU_THE_GUARDIANS = 5
    DIAKFU = 6
    WAKFU_THE_GUARDIANS_2 = 7
    BOUFBOWL = 8
    KROSMASTER = 9
    KROSMASTER_ARENA = 10
    TACTILE_WARS = 11
    FLYN = 12
    KROSMASTER_3D = 13
    KWAAN = 14
    ABRACA = 15
    KING_TONGUE = 16
    KROSMAGA = 17
    DOFUS_TOUCH = 18
    DRAKERZ = 19
    DOFUS_PETS = 20
    DOFUS_3 = 21
    WAVEN = 22
    CHAT = 99
    UPDATER = 100
    DOFUS_FRIGOST_BETA = 101
    ZAAP = 102
    ANKAMA_WEBSITE = 103
    FORUM = 999
    DOFUS_2_BETA = 1001
    DOFUS_ARENA_BETA = 1002
    DOFUS_ARENA_BETA_2 = 1004
    DOFUS_2_FRIGOST_BETA = 1005
    DOFUS_2_FRIGOST_EP2_BETA = 1006
    WAKFU_TEST = 3001
    WAKFU_HEROES = 3002
    KROSMASTER_ARENA_BETA = 10001
    TACTILE_WARS_TEST = 11001
    KROSMASTER_3D_BETA = 13001

    # Names associated with game IDs
    _names = {
        DOFUS: "Dofus",
        DOFUS_ARENA: "Dofus Arena",
        WAKFU: "Wakfu",
        DOFUS_POCKET: "Dofus Pocket",
        WAKFU_THE_GUARDIANS: "Wakfu - The Guardians",
        DIAKFU: "Diakfu",
        WAKFU_THE_GUARDIANS_2: "Wakfu - The Guardians 2",
        BOUFBOWL: "Boufbowl",
        KROSMASTER: "Krosmaster",
        KROSMASTER_ARENA: "Krosmaster Arena",
        TACTILE_WARS: "Tactile Wars",
        FLYN: "Fly'N",
        KROSMASTER_3D: "Krosmaster 3D",
        KWAAN: "Kwaan",
        ABRACA: "Abraca",
        KING_TONGUE: "King Tongue",
        KROSMAGA: "Krosmaga",
        DOFUS_TOUCH: "Dofus Touch",
        DRAKERZ: "Drakerz",
        DOFUS_PETS: "Dofus Pets",
        DOFUS_3: "Dofus 3",
        WAVEN: "Waven",
        CHAT: "Chat",
        UPDATER: "Updater",
        DOFUS_FRIGOST_BETA: "Dofus Frigost - Beta",
        ZAAP: "Ankama Launcher",
        ANKAMA_WEBSITE: "Website Ankama",
        FORUM: "Forum",
        DOFUS_2_BETA: "Dofus 2 - Beta",
        DOFUS_ARENA_BETA: "Dofus Arena - Beta",
        DOFUS_ARENA_BETA_2: "Dofus Arena - Beta 2",
        DOFUS_2_FRIGOST_BETA: "Dofus 2 Frigost - Beta",
        DOFUS_2_FRIGOST_EP2_BETA: "Dofus 2 Frigost Ep.2 - Beta",
        WAKFU_TEST: "Wakfu - Test",
        WAKFU_HEROES: "Wakfu Heroes",
        KROSMASTER_ARENA_BETA: "Krosmaster Arena - Beta",
        TACTILE_WARS_TEST: "Tactile Wars - Test",
        KROSMASTER_3D_BETA: "Krosmaster 3D - Beta",
    }

    @staticmethod
    @property
    def current():
        return GameID.DOFUS

    @staticmethod
    def getName(value):
        return GameID._names.get(value, "Unknown")
