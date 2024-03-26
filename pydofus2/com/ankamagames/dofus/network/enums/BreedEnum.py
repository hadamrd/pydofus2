class BreedEnum:

    UNDEFINED: int = 0

    Feca: int = 1

    Osamodas: int = 2

    Enutrof: int = 3

    Sram: int = 4

    Xelor: int = 5

    Ecaflip: int = 6

    Eniripsa: int = 7

    Iop: int = 8

    Cra: int = 9

    Sadida: int = 10

    Sacrieur: int = 11

    Pandawa: int = 12

    Roublard: int = 13

    Zobal: int = 14

    Steamer: int = 15

    Eliotrope: int = 16

    Huppermage: int = 17

    Ouginak: int = 18

    SUMMONED: int = -1

    MONSTER: int = -2

    MONSTER_GROUP: int = -3

    NPC: int = -4

    HUMAN_VENDOR: int = -5

    TAX_COLLECTOR: int = -6

    MUTANT: int = -7

    MUTANT_IN_DUNGEON: int = -8

    MOUNT_OUTSIDE: int = -9

    PRISM: int = -10

    INCARNATION: int = -11

    @classmethod
    def get_name(cls, breedId):
        if breedId == cls.UNDEFINED:
            return "UNDEFINED"
        if breedId == cls.Feca:
            return "Feca"
        if breedId == cls.Osamodas:
            return "Osamodas"
        if breedId == cls.Enutrof:
            return "Enutrof"
        if breedId == cls.Sram:
            return "Sram"
        if breedId == cls.Xelor:
            return "Xelor"
        if breedId == cls.Ecaflip:
            return "Ecaflip"
        if breedId == cls.Eniripsa:
            return "Eniripsa"
        if breedId == cls.Iop:
            return "Iop"
        if breedId == cls.Cra:
            return "Cra"
        if breedId == cls.Sadida:
            return "Sadida"
        if breedId == cls.Sacrieur:
            return "Sacrieur"
        if breedId == cls.Pandawa:
            return "Pandawa"
        if breedId == cls.Roublard:
            return "Roublard"
        if breedId == cls.Zobal:
            return "Zobal"
        if breedId == cls.Steamer:
            return "Steamer"
        if breedId == cls.Eliotrope:
            return "Eliotrope"
        if breedId == cls.Huppermage:
            return "Huppermage"
        if breedId == cls.Ouginak:
            return "Ouginak"
        if breedId == cls.SUMMONED:
            return "SUMMONED"
        if breedId == cls.MONSTER:
            return "MONSTER"
        if breedId == cls.MONSTER_GROUP:
            return "MONSTER_GROUP"
        if breedId == cls.NPC:
            return "NPC"
        if breedId == cls.HUMAN_VENDOR:
            return "HUMAN_VENDOR"
        if breedId == cls.TAX_COLLECTOR:
            return "TAX_COLLECTOR"
        if breedId == cls.MUTANT:
            return "MUTANT"
        if breedId == cls.MUTANT_IN_DUNGEON:
            return "MUTANT_IN_DUNGEON"
        if breedId == cls.MOUNT_OUTSIDE:
            return "MOUNT_OUTSIDE"
        if breedId == cls.PRISM:
            return "PRISM"
        if breedId == cls.INCARNATION:
            return "INCARNATION"
        return "Unknown breedId"
