from enum import Enum


class DisconnectionReasonEnum(Enum):

    RESTARTING: int = 6

    UNEXPECTED: int = 0

    SWITCHING_TO_GAME_SERVER: int = 1

    SWITCHING_TO_HUMAN_VENDOR: int = 2

    DISCONNECTED_BY_POPUP_WITHOUT_RESET: int = 5

    DISCONNECTED_BY_POPUP: int = 3
    
    DISCONNECTED_BY_USER = 11
    
    NEVER_CONNECTED: int = 4

    WANTED_SHUTDOWN = 7

    EXCEPTION_THROWN = 8

    CONNECTION_LOST = 9
    
    CHANGING_SERVER = 10
    
    CONNECTION_PROCESS_CRASHED = 11
    
    BANNED = 12
    
    
