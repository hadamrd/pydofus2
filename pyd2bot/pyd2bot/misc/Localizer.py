import json
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from pydofus2.com.ankamagames.dofus.datacenter.world.Phoenix import Phoenix
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.astar.AStar import AStar
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.WorldPathFinder import WorldPathFinder
from pyd2bot.BotConstants import BotConstants


class BankInfos:
    def __init__(self, npcActionId: int, npcId: float, npcMapId: float, openBankReplyId: int, name: str = "undefined"):
        self.name = name
        self.npcActionId = npcActionId
        self.npcId = npcId
        self.npcMapId = npcMapId
        self.openBankReplyId = openBankReplyId

    def to_json(self):
        return {
            "npcActionId": self.npcActionId,
            "npcId": self.npcId,
            "npcMapId": self.npcMapId,
            "openBankReplyId": self.openBankReplyId
        }


class Localizer:
    _phenixesByAreaId = dict[int, list]()
    with open(BotConstants.PERSISTENCE_DIR / "areaInfos.json", "r") as f:
        AREAINFOS: dict = json.load(f)

    @classmethod
    def getBankInfos(cls) -> BankInfos:
        subareaId = MapDisplayManager().currentDataMap.subareaId
        subarea = SubArea.getSubAreaById(subareaId)
        areaId = subarea._area.id
        playerPos = PlayedCharacterManager().currMapPos
        minDist = float("inf")
        srcV = WorldPathFinder().currPlayerVertex
        closestBank = None
        rpZ = 1
        for bank in cls.AREAINFOS[str(areaId)]["bank"]:
            bankMapId = bank["npcMapId"]
            while True:
                dstV = WorldPathFinder().worldGraph.getVertex(bankMapId, rpZ)
                if not dstV:
                    break
                path = AStar.search(WorldPathFinder().worldGraph, srcV, dstV, lambda x: (), False)
                if path is not None:
                    dist = len(path)
                    if dist < minDist:
                        minDist = dist
                        closestBank = bank
                    break
                rpZ += 1
        return BankInfos(**closestBank)

    @classmethod
    def getPhenixMapId(cls) -> float:
        subareaId = MapDisplayManager().currentDataMap.subareaId
        subarea = SubArea.getSubAreaById(subareaId)
        areaId = subarea._area.id
        return cls.AREAINFOS[str(areaId)]["phoenix"]["mapId"]
