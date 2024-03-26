from enum import Enum


class RequestTypesEnum(Enum):
    MOVE = 1
    ATTACK_MONSTERS = 2
    MAP_CHANGE = 3
    USE_SKILL = 4
    JOIN_FIGHT = 5
