class TreasureHuntStepTypeEnum:
    START = 0
    DIRECTION_TO_POI = 1
    DIRECTION_TO_HINT = 5
    FIGHT = 2
    DIRECTION = 3
    UNKNOWN = 4

    @staticmethod
    def to_string(type):
        if type == TreasureHuntStepTypeEnum.START:
            return "Start"
        elif type == TreasureHuntStepTypeEnum.DIRECTION_TO_POI:
            return "Direction to POI"
        elif type == TreasureHuntStepTypeEnum.DIRECTION_TO_HINT:
            return "Direction to Hint"
        elif type == TreasureHuntStepTypeEnum.FIGHT:
            return "Fight"
        elif type == TreasureHuntStepTypeEnum.DIRECTION:
            return "Direction"
        elif type == TreasureHuntStepTypeEnum.UNKNOWN:
            return "Unknown"
        else:
            return "Invalid Type"
