from datetime import datetime
from typing import List

from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class ServerSeason(IDataCenter):
    MODULE = "ServerSeasons"

    def __init__(self):
        self.uid: int
        self.seasonNumber: int
        self.information: str
        self.beginning: float
        self.closure: float
        self.resetDate: float
        self.flagObjectId: int

    @classmethod
    def getSeasonById(cls, id: int) -> "ServerSeason":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getAllSeason(cls) -> List["ServerSeason"]:
        return GameData().getObjects(cls.MODULE)

    @staticmethod
    def getCurrentSeason() -> "ServerSeason":
        allSeasons = ServerSeason.getAllSeason()
        currentTimestamp = datetime.now().timestamp()
        for season in allSeasons:
            if season.resetDate <= season.closure:
                if season.beginning <= currentTimestamp <= season.closure:
                    return season
            else:
                if season.beginning <= currentTimestamp <= season.resetDate:
                    return season
        return None

    def isFinished(self) -> bool:
        currentTimestamp = datetime.now().timestamp()
        return currentTimestamp > self.closure
