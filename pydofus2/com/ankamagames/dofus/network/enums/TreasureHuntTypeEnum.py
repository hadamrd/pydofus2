class TreasureHuntTypeEnum:
    TREASURE_HUNT_CLASSIC = 0
    TREASURE_HUNT_PORTAL = 1
    TREASURE_HUNT_LEGENDARY = 2

    @staticmethod
    def to_string(type):
        if type == TreasureHuntTypeEnum.TREASURE_HUNT_CLASSIC:
            return "Classic"
        elif type == TreasureHuntTypeEnum.TREASURE_HUNT_PORTAL:
            return "Portal"
        elif type == TreasureHuntTypeEnum.TREASURE_HUNT_LEGENDARY:
            return "Legendary"
        else:
            return "Invalid Type"
