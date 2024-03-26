class TreasureHuntFlagStateEnum:
    TREASURE_HUNT_FLAG_STATE_UNKNOWN = 0
    TREASURE_HUNT_FLAG_STATE_OK = 1
    TREASURE_HUNT_FLAG_STATE_WRONG = 2
    TREASURE_HUNT_FLAG_STATE_UNSUBMITTED = -1

    def to_string(state):
        if state == TreasureHuntFlagStateEnum.TREASURE_HUNT_FLAG_STATE_UNKNOWN:
            return "Unknown"
        elif state == TreasureHuntFlagStateEnum.TREASURE_HUNT_FLAG_STATE_OK:
            return "OK"
        elif state == TreasureHuntFlagStateEnum.TREASURE_HUNT_FLAG_STATE_WRONG:
            return "Wrong"
        else:
            return "N/A"
