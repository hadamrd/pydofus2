class GameActionFightInvisibilityStateEnum:
    INVISIBLE: int = 1
    DETECTED: int = 2
    VISIBLE: int = 3

    @classmethod
    def getStateName(cls, state: int) -> str:
        if state == cls.INVISIBLE:
            return "invisible"
        if state == cls.DETECTED:
            return "detected"
        if state == cls.VISIBLE:
            return "visible"
        return "unknown"
