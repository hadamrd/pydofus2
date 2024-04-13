from pydofus2.com.ankamagames.dofus.datacenter.world.Area import Area
from pydofus2.com.ankamagames.dofus.datacenter.world.Hint import Hint
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.world.WorldPointWrapper import WorldPointWrapper
from pydofus2.com.ankamagames.dofus.network.enums.TeleporterTypeEnum import TeleporterTypeEnum
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class TeleportDestinationWrapper(IDataCenter):
    _hints = {}
    _hintsRealMap = dict[int, list]()

    def __init__(
        self,
        teleporterGenericType,
        mapId,
        subareaId,
        destType,
        level,
        cost,
        spawn=False,
        hint: Hint = None,
        known=True,
    ):
        super().__init__()
        self.teleporterType = teleporterGenericType
        self.mapId = mapId
        self.subArea = SubArea.getSubAreaById(subareaId)
        self.subAreaName = self.subArea.name
        self.destinationType = destType
        self.level = level
        self.cost = cost
        self.spawn = spawn
        self.known = known
        if self.teleporterType == TeleporterTypeEnum.TELEPORTER_SUBWAY:
            if hint:
                self.category = hint.categoryId
                self.areaName = hint.name
                self.nameId = hint.nameId
            else:
                self.category = -1
        else:
            area = Area.getAreaById(self.subArea.areaId)
            self.areaName = area.name
            self.nameId = area.nameId
            self.subAreaNameId = self.subArea.nameId
        p = WorldPointWrapper(mapId)
        self.coord = f"{p.outdoorX},{p.outdoorY}"

    @classmethod
    def getHintsFromMapId(cls, mapId) -> list[Hint]:
        ret = []
        cls.generateHintsDictionary()
        if mapId in cls._hintsRealMap:
            ret = cls._hintsRealMap[mapId]
        if mapId in cls._hints:
            return ret + cls._hints[mapId]
        return ret

    @classmethod
    def generateHintsDictionary(cls):
        hints = Hint.getHints()
        if not cls._hints:
            cls._hints = dict[int, list]()
            cls._hintsRealMap = dict[int, list]()
            for hint in hints:
                if hint.mapId in cls._hints:
                    cls._hints[hint.mapId].append(hint)
                else:
                    cls._hints[hint.mapId] = [hint]
                if hint.realMapId in cls._hintsRealMap:
                    cls._hintsRealMap[hint.realMapId].append(hint)
                else:
                    cls._hintsRealMap[hint.realMapId] = [hint]
