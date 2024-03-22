from pydofus2.com.ankamagames.dofus.datacenter.npcs.Npc import Npc
from pydofus2.com.ankamagames.dofus.datacenter.quest.treasureHunt.PointOfInterest import \
    PointOfInterest
from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import \
    MapPosition
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.datacenter.world.WorldMap import WorldMap
from pydofus2.com.ankamagames.dofus.internalDatacenter.world.WorldPointWrapper import \
    WorldPointWrapper
from pydofus2.com.ankamagames.dofus.types.enums.TreasureHuntStepTypeEnum import \
    TreasureHuntStepTypeEnum
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import \
    DirectionsEnum
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import \
    PatternDecoder


class TreasureHuntStepWrapper(IDataCenter):
    def __init__(self):
        self.index = 0
        self.type = 0
        self.direction = -1
        self.mapId = -1
        self.poiLabel = 0
        self.flagState = -1
        self.count = 0
        self._stepText = None
        self._stepRolloverText = None

    @staticmethod
    def create(type, index, direction, mapId, poiLabel, flagState=-1, count=0):
        item = TreasureHuntStepWrapper()
        item.type = type
        item.index = index
        item.direction = direction
        item.mapId = mapId
        item.poiLabel = poiLabel
        item.flagState = flagState
        item.count = count
        return item

    @property
    def text(self):
        if not self._stepText:
            if self.type == TreasureHuntStepTypeEnum.START:
                map = WorldPointWrapper(self.mapId)
                self._stepText = I18n.getUiText("ui.common.start") + " [" + str(map.outdoorX) + "," + str(map.outdoorY) + "]"
                p = MapPosition.getMapPositionById(self.mapId)
                if p and p.worldMap > 1:
                    wm = WorldMap.getWorldMapById(p.worldMap)
                    self._stepText += " " + wm.name if wm else ""
            elif self.type == TreasureHuntStepTypeEnum.DIRECTION_TO_POI:
                poi = PointOfInterest.getPointOfInterestById(self.poiLabel)
                self._stepText = poi.name if poi else "???"
            elif self.type == TreasureHuntStepTypeEnum.DIRECTION:
                self._stepText = "x" + str(self.count)
            elif self.type == TreasureHuntStepTypeEnum.DIRECTION_TO_HINT:
                npc = Npc.getNpcById(self.count)
                self._stepText = npc.name
            elif self.type == TreasureHuntStepTypeEnum.FIGHT:
                self._stepText = ""
            elif self.type == TreasureHuntStepTypeEnum.UNKNOWN:
                self._stepText = "?"
        return self._stepText

    @property
    def overText(self):
        if not self._stepRolloverText:
            if self.type == TreasureHuntStepTypeEnum.START:
                subArea = SubArea.getSubAreaByMapId(self.mapId)
                if subArea:
                    area = subArea.area
                    if area:
                        self._stepRolloverText = area.name + " (" + subArea.name + ")"
            elif self.type == TreasureHuntStepTypeEnum.DIRECTION_TO_POI or self.type == TreasureHuntStepTypeEnum.DIRECTION_TO_HINT:
                directionName = DirectionsEnum(self.direction).name
                self._stepRolloverText = I18n.getUiText("ui.treasureHunt.followDirectionToPOI", [directionName, "[" + self._stepText + "]"])
            elif self.type == TreasureHuntStepTypeEnum.DIRECTION:
                directionName = DirectionsEnum(self.direction).name
                self._stepRolloverText = PatternDecoder.combine(I18n.getUiText("ui.treasureHunt.followDirection", [self.count, directionName]), "n", self.count <= 1)
        return self._stepRolloverText

    def update(self, type, index, direction, mapId, poiLabel, flagState=-1, count=0):
        self.type = type
        self.index = index
        self.direction = direction
        self.mapId = mapId
        self.poiLabel = poiLabel
        self.flagState = flagState
        self.count = count

    def __repr__(self) -> str:
        return (
            f"TreasureHuntStepWrapper(type={self.type}, "
            f"index={self.index}, "
            f"direction={self.direction}, "
            f"mapId={self.mapId}, "
            f"poiLabel={self.poiLabel}, "
            f"flagState={self.flagState}, "
            f"count={self.count})"
        )