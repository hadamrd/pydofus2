from typing import Dict

from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel

class AccountManager:
    _singleton = None

    def __init__(self):
        self._accounts: Dict[str, dict] = {}
        self.achievementPoints: int = 0
        self.achievementPercent: int = 0

    @classmethod
    def getInstance(cls):
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton

    def getIsKnowAccount(self, playerName: str) -> bool:
        return playerName in self._accounts

    def getAccountId(self, playerName: str) -> int:
        if playerName in self._accounts:
            return self._accounts[playerName]["id"]
        return 0

    def getAccountName(self, playerName: str) -> str:
        if playerName in self._accounts:
            return self._accounts[playerName]["name"]
        return ""

    def setAccount(self, playerName: str, accountId: int, accountName: str = None, accountTag: str = None):
        self._accounts[playerName] = {"id": accountId, "name": accountName, "tag": accountTag}

    def setAccountFromId(self, playerId: float, accountId: int, accountName: str = None):
        _roleplayEntityFrame = Kernel().roleplayEntitiesFrame
        
        if _roleplayEntityFrame:
            entityInfo = _roleplayEntityFrame.getEntityInfos(playerId)
            if entityInfo:
                self._accounts[entityInfo.name] = {"id": accountId, "name": accountName}
        else:
            _fightEntityFrame = Kernel().fightEntitiesFrame
            if _fightEntityFrame:
                fightInfo = _fightEntityFrame.getEntityInfos(playerId)
                if fightInfo:
                    self._accounts[fightInfo.name] = {"id": accountId, "name": accountName}
