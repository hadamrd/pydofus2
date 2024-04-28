from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton


class GameDebugManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.buffsDebugActivated: bool = False
        self.detailedFightLog_showEverything: bool = False
        self.detailedFightLog_showBuffsInUi: bool = False
        super().__init__()
