from enum import Enum, auto


class MovementFailError(Enum):
    PLAYER_IS_DEAD = auto()
    CANT_REACH_DEST_CELL = auto()
    ALREADY_REQUESTING_MOVEMENT = auto()
    ALREADY_MOVING = auto()
    PLAYER_NOT_FOUND = auto()
    MAP_NOT_LOADED = auto()
    PLAYER_CANT_MOVE = auto()
    MOVE_REQUEST_TIMEOUT = auto()
    MOVE_REQUEST_REJECTED = auto()
    MAP_CHANGE_TIMEOUT = auto()
    INTERACTIVE_USE_ERROR = auto()
    NO_PATH_FOUND = auto()
    NO_VALID_SCROLL_CELL = auto()
    INVALID_TRANSITION = auto()
