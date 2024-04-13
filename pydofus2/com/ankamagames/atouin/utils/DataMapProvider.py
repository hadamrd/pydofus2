from typing import TYPE_CHECKING

import pydofus2.com.ankamagames.atouin.managers.MapDisplayManager as mdmm
from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import EntitiesManager
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.interfaces.IObstacle import IObstacle
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.mapTools import MapTools

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell


class DataMapProvider(IDataMapProvider, metaclass=Singleton):
    TOLERANCE_ELEVATION = 11

    def __init__(self):
        super().__init__()
        self.obstaclesCells = list[int]()
        self._updatedCell = dict()
        self._specialEffects = dict()
        self.isInFight = False
        self._playerobject = AnimatedCharacter

    def pointLos(self, x: int, y: int, allowTroughEntity: bool = True) -> bool:
        cellId = MapTools.getCellIdByCoord(x, y)
        los = mdmm.MapDisplayManager().currentDataMap.cells[cellId].los
        if cellId in self._updatedCell:
            los = self._updatedCell[cellId]
        if not allowTroughEntity:
            cellEntities = EntitiesManager().getEntitiesOnCell(cellId, IObstacle)
            for o in cellEntities:
                if not o.canSeeThrough:
                    return False
        return los

    def farmCell(self, x: int, y: int) -> bool:
        cellId: int = MapTools.getCellIdByCoord(x, y)
        return mdmm.MapDisplayManager().currentDataMap.cells[cellId].farmCell

    def cellByIdIsHavenbagCell(self, cellId: int) -> bool:
        return mdmm.MapDisplayManager().currentDataMap.cells[cellId].havenbagCell

    def cellByCoordsIsHavenbagCell(self, x: int, y: int) -> bool:
        cellId: int = MapTools.getCellIdByCoord(x, y)
        return mdmm.MapDisplayManager().currentDataMap.cells[cellId].havenbagCell

    def isChangeZone(self, cell1: int, cell2: int) -> bool:
        cellData1 = mdmm.MapDisplayManager().currentDataMap.cells[cell1]
        cellData2 = mdmm.MapDisplayManager().currentDataMap.cells[cell2]
        diff = abs(abs(cellData1.floor) - abs(cellData2.floor))
        return cellData1.moveZone != cellData2.moveZone and diff == 0

    def pointMov(
        self,
        x: int,
        y: int,
        bAllowTroughEntity: bool = True,
        previousCellId: int = -1,
        endCellId: int = -1,
        avoidObstacles: bool = True,
        dataMap=None,
    ) -> bool:
        mov = False
        if MapPoint.isInMap(x, y):
            if not dataMap:
                dataMap = mdmm.MapDisplayManager().dataMap
            useNewSystem = dataMap.isUsingNewMovementSystem
            cellId = MapTools.getCellIdByCoord(x, y)
            cellData = dataMap.cells[cellId]
            mov = cellData.mov and not (self.isInFight and cellData.nonWalkableDuringFight)
            if mov and cellId in self._updatedCell:
                mov = self._updatedCell[cellId]
            if mov and useNewSystem and previousCellId != -1 and previousCellId != cellId:
                previousCellData = dataMap.cells[previousCellId]
                diff = abs(abs(cellData.floor) - abs(previousCellData.floor))
                if (previousCellData.moveZone != cellData.moveZone and diff > 0) or (
                    previousCellData.moveZone == cellData.moveZone
                    and cellData.moveZone == 0
                    and diff > self.TOLERANCE_ELEVATION
                ):
                    return False
            if mov and not bAllowTroughEntity:
                for entity in EntitiesManager().entities.values():
                    if isinstance(entity, IObstacle) and entity.position and entity.position.cellId == cellId:
                        if not (endCellId == cellId and entity.canWalkTo):
                            if not entity.canWalkThrough:
                                return False
                if avoidObstacles and (cellId in self.obstaclesCells and cellId != endCellId):
                    return False
            return mov
        else:
            return False

    def pointCanStop(self, x: int, y: int, bAllowTroughEntity: bool = True) -> bool:
        cellId: int = MapTools.getCellIdByCoord(x, y)
        cellData: "Cell" = mdmm.MapDisplayManager().currentDataMap.cells[cellId]
        return self.pointMov(x, y, bAllowTroughEntity) and (self.isInFight or not cellData.nonWalkableDuringRP)

    def fillEntityOnCellArray(self, v: list[bool], allowThroughEntity: bool) -> list[bool]:
        for e in EntitiesManager().entities.values():
            if (
                isinstance(e, self._playerobject)
                and (not allowThroughEntity or not e.canWalkThrough)
                and e.position is not None
            ):
                v[e.position.cellId] = True
        return v

    def pointWeight(self, x: int, y: int, bAllowTroughEntity: bool = True) -> float:
        weight: float = 1
        cellId: int = MapTools.getCellIdByCoord(x, y)
        speed: int = self.getCellSpeed(cellId)
        if bAllowTroughEntity:
            if speed >= 0:
                weight += 5 - speed
            else:
                weight += 11 + abs(speed)
            entity = EntitiesManager().getEntityOnCell(cellId, self._playerobject)
            if entity:
                weight = 20
            else:
                if EntitiesManager().getEntityOnCell(cellId, self._playerobject) is not None:
                    weight += 0.3
                if (
                    EntitiesManager().getEntityOnCell(MapTools.getCellIdByCoord(x + 1, y), self._playerobject)
                    is not None
                ):
                    weight += 0.3
                if (
                    EntitiesManager().getEntityOnCell(MapTools.getCellIdByCoord(x, y + 1), self._playerobject)
                    is not None
                ):
                    weight += 0.3
                if (
                    EntitiesManager().getEntityOnCell(MapTools.getCellIdByCoord(x - 1, y), self._playerobject)
                    is not None
                ):
                    weight += 0.3
                if (
                    EntitiesManager().getEntityOnCell(MapTools.getCellIdByCoord(x, y - 1), self._playerobject)
                    is not None
                ):
                    weight += 0.3
                if (self.pointSpecialEffects(x, y) & 2) == 2:
                    weight += 0.2
        return weight

    def getCellSpeed(self, cellId: int) -> int:
        return mdmm.MapDisplayManager().currentDataMap.cells[cellId].speed

    def pointSpecialEffects(self, x: int, y: int) -> int:
        cellId: int = MapTools.getCellIdByCoord(x, y)
        if self._specialEffects.get(cellId):
            return self._specialEffects[cellId]
        return 0

    @property
    def width(self) -> int:
        return AtouinConstants.MAP_HEIGHT + AtouinConstants.MAP_WIDTH - 2

    @property
    def height(self) -> int:
        return AtouinConstants.MAP_HEIGHT + AtouinConstants.MAP_WIDTH - 1

    def hasEntity(self, x: int, y: int, bAllowTroughEntity: bool = False) -> bool:
        cellEntities: list[IObstacle] = EntitiesManager().getEntitiesOnCell(MapTools.getCellIdByCoord(x, y), IObstacle)
        for o in cellEntities:
            if not (o.canWalkTo or (bAllowTroughEntity and o.canSeeThrough)):
                return True
        return False

    def updateCellMovLov(self, cellId: int, canMove: bool) -> None:
        self._updatedCell[cellId] = canMove

    def resetUpdatedCell(self) -> None:
        self._updatedCell.clear()

    def setSpecialEffects(self, cellId: int, value: int) -> None:
        self._specialEffects[cellId] = value

    def resetSpecialEffects(self) -> None:
        self._specialEffects.clear()
