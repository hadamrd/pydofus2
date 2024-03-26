class ElementEnum:

    ELEMENT_MULTI: int = -2

    ELEMENT_UNDEFINED: int = -1

    ELEMENT_NEUTRAL: int = 0

    ELEMENT_EARTH: int = 1

    ELEMENT_FIRE: int = 2

    ELEMENT_WATER: int = 3

    ELEMENT_AIR: int = 4

    ELEMENT_NONE: int = 5

    ELEMENT_BEST: int = 6

    _values_for_1 = {82, 89, 95, 100, 143, 144, 279, 671, 672, 1012, 1071, 1092, 1124, 1224, 3001}
    _values_for_2 = {86, 92, 97, 276, 1016, 1063, 1070, 1096, 1128, 1228, 3000}
    _values_for_3 = {88, 94, 99, 108, 278, 1015, 1037, 1066, 1069, 1094, 1126, 1226}
    _values_for_4 = {87, 93, 98, 277, 1013, 1064, 1067, 1093, 1125, 1225, 2999}
    _values_for_5 = {81}
    _values_for_6 = {2822, 2828, 2829, 2830, 3002}
    _values_for_7 = {2832, 2890, 2891}

    def __init__(self):
        pass

    @classmethod
    def getElementFromActionId(cls, actionId: int) -> int:
        if actionId in cls._values_for_1:
            return 1
        elif actionId in cls._values_for_2:
            return 2
        elif actionId in cls._values_for_3:
            return 3
        elif actionId in cls._values_for_4:
            return 4
        if actionId in cls._values_for_5:
            return 5
        elif actionId in cls._values_for_6:
            return 6
        elif actionId in cls._values_for_7:
            return 7
        else:
            return -1
