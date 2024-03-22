import heapq

import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import \
    DataMapProvider
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.TransitionTypeEnum import \
    TransitionTypeEnum
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.WorldGraph import \
    WorldGraph
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.positions.MovementPath import \
    MovementPath
from pydofus2.com.ankamagames.jerakine.types.positions.PathElement import \
    PathElement


class Pathfinding(metaclass=Singleton):
    VERBOSE = False
    HV_COST: int = 10
    DIAG_COST: int = 15
    HEURISTIC_SCALE: int = 10
    INFINITE_COST: int = float("inf")

    def __init__(self):
        super().__init__()

    def isChild(self, x, y, parentId) -> bool:
        cellId = MapTools.getCellIdByCoord(x, y)
        parentX = MapTools.getCellIdXCoord(parentId)
        parentY = MapTools.getCellIdYCoord(parentId)
        canMoveFromParentToEnd = self.pointMov(x, y, parentId)
        return (
            cellId is not None
            and cellId not in self._isCellClosed
            and cellId != parentId
            and canMoveFromParentToEnd
            and (
                y == parentY
                or x == parentX
                or self._allowDiag
                and (
                    self._mapData.pointMov(parentX, y, self._allowTroughEntity, parentId)
                    or self._mapData.pointMov(x, parentY, self._allowTroughEntity, parentId)
                )
            )
        )

    def initAlgo(self, start: MapPoint, end: MapPoint, allowDiag, bAllowTroughEntity, avoidObstacles):
        self._allowDiag = allowDiag
        self._allowTroughEntity = bAllowTroughEntity
        self._avoidObstacles = avoidObstacles
        self._end = end
        self._start = start
        self._mapData = DataMapProvider()
        self._parentOfCell = {}
        self._isCellClosed = set()
        self._isEntityOnCell = {}
        self._costOfCell = {}
        self._costOfCell[self._start.cellId] = 0
        self._endCellAuxId = start.cellId
        self._distToEnd = self.distFromEnd(start.cellId)
        self._mapData.fillEntityOnCellArray(self._isEntityOnCell, bAllowTroughEntity)

    def distFromStart(self, cellId):
        return self._start.distanceToCellId(cellId)

    def distFromEnd(self, cellId):
        return self._end.distanceToCellId(cellId)

    def moveCost(self, x, y, parentId):
        cellId = MapTools.getCellIdByCoord(x, y)
        pointWeight = self.getMapPointWeight(x, y)
        parentX = MapTools.getCellIdXCoord(parentId)
        parentY = MapTools.getCellIdYCoord(parentId)
        movementCost = (
            self._costOfCell[parentId]
            + (self.HV_COST if y == parentY or x == parentX else self.DIAG_COST) * pointWeight
        )
        if self._allowTroughEntity:
            cellOnEndColumn = x + y == self._end.y + self._end.y
            cellOnStartColumn = x + y == self._start.x + self._start.y
            cellOnEndLine = x - y == self._end.x - self._end.y
            cellOnStartLine = x - y == self._start.x - self._start.y
            if not cellOnEndColumn and not cellOnEndLine or not cellOnStartColumn and not cellOnStartLine:
                movementCost += self.distFromEnd(cellId)
                movementCost += self.distFromStart(cellId)
            if x == self._end.x or y == self._end.y:
                movementCost -= 3
            if cellOnEndColumn or cellOnEndLine or x + y == parentX + parentY or x - y == parentX - parentY:
                movementCost -= 2
            if x == self._start.x or y == self._start.y:
                movementCost -= 3
            if cellOnStartColumn or cellOnStartLine:
                movementCost -= 2
        return movementCost

    def iterChilds(self, parentId):
        parentX = MapTools.getCellIdXCoord(parentId)
        parentY = MapTools.getCellIdYCoord(parentId)
        for y in range(parentY - 1, parentY + 2):
            for x in range(parentX - 1, parentX + 2):
                if self.isChild(x, y, parentId):
                    yield x, y

    def pointMov(self, x, y, dstCell):
        return self._mapData.pointMov(x, y, self._allowTroughEntity, dstCell, self._end.cellId, self._avoidObstacles)

    def buildPath(self):
        movPath: MovementPath = MovementPath()
        movPath.start = self._start
        cursor = self._end.cellId
        if self._parentOfCell.get(self._end.cellId) is None:
            cursor = self._endCellAuxId
            movPath.end = MapPoint.fromCellId(self._endCellAuxId)
        else:
            movPath.end = self._end
        while cursor != self._start.cellId:
            if self._allowDiag:
                parent = self._parentOfCell.get(cursor)
                grandParent = self._parentOfCell.get(parent)
                grandGrandParent = self._parentOfCell.get(grandParent)
                kX = MapTools.getCellIdXCoord(cursor)
                kY = MapTools.getCellIdYCoord(cursor)
                if grandParent is not None and MapTools.getDistance(cursor, grandParent) == 1:
                    if self.pointMov(kX, kY, grandParent):
                        self._parentOfCell[cursor] = grandParent
                elif grandGrandParent is not None and MapTools.getDistance(cursor, grandGrandParent) == 2:
                    nextX = MapTools.getCellIdXCoord(grandGrandParent)
                    nextY = MapTools.getCellIdYCoord(grandGrandParent)
                    interX = kX + round((nextX - kX) / 2)
                    interY = kY + round((nextY - kY) / 2)
                    if self.pointMov(interX, interY, cursor) and self._mapData.pointWeight(interX, interY) < 2:
                        self._parentOfCell[cursor] = MapTools.getCellIdByCoord(interX, interY)
                elif grandParent is not None and MapTools.getDistance(cursor, grandParent) == 2:
                    nextX = MapTools.getCellIdXCoord(grandParent)
                    nextY = MapTools.getCellIdYCoord(grandParent)
                    interX = MapTools.getCellIdXCoord(parent)
                    interY = MapTools.getCellIdYCoord(parent)
                    if (
                        kX + kY == nextX + nextY
                        and kX - kY != interX - interY
                        and not self._mapData.isChangeZone(
                            MapTools.getCellIdByCoord(kX, kY),
                            MapTools.getCellIdByCoord(interX, interY),
                        )
                        and not self._mapData.isChangeZone(
                            MapTools.getCellIdByCoord(interX, interY),
                            MapTools.getCellIdByCoord(nextX, nextY),
                        )
                    ):
                        self._parentOfCell[cursor] = grandParent
                    elif (
                        kX - kY == nextX - nextY
                        and kX - kY != interX - interY
                        and not self._mapData.isChangeZone(
                            MapTools.getCellIdByCoord(kX, kY),
                            MapTools.getCellIdByCoord(interX, interY),
                        )
                        and not self._mapData.isChangeZone(
                            MapTools.getCellIdByCoord(interX, interY),
                            MapTools.getCellIdByCoord(nextX, nextY),
                        )
                    ):
                        self._parentOfCell[cursor] = grandParent
                    elif (
                        kX == nextX
                        and kX != interX
                        and self._mapData.pointWeight(kX, interY) < 2
                        and self._mapData.pointMov(kX, interY, cursor)
                    ):
                        self._parentOfCell[cursor] = MapTools.getCellIdByCoord(kX, interY)
                    elif (
                        kY == nextY
                        and kY != interY
                        and self._mapData.pointWeight(interX, kY) < 2
                        and self._mapData.pointMov(interX, kY, cursor)
                    ):
                        self._parentOfCell[cursor] = MapTools.getCellIdByCoord(interX, kY)
            movPath.addPoint(
                PathElement(
                    MapPoint.fromCellId(self._parentOfCell[cursor]),
                    MapTools.getLookDirection8Exact(self._parentOfCell[cursor], cursor),
                )
            )
            cursor = self._parentOfCell[cursor]
        movPath.path.reverse()
        return movPath

    def getCurrentMapInteractiveTrCells(self):
        res = []
        currVertex = PlayedCharacterManager().currVertex
        if not currVertex:
            return res
        for edge in WorldGraph().getOutgoingEdgesFromVertex(currVertex):
            for tr in edge.transitions:
                if TransitionTypeEnum(tr.type) == TransitionTypeEnum.INTERACTIVE:
                    res.append(tr.cell)
        return res

    def getCurrentMapActionCells(self):
        res = []
        currVertex = PlayedCharacterManager().currVertex
        if not currVertex:
            return res
        for edge in WorldGraph().getOutgoingEdgesFromVertex(currVertex):
            for tr in edge.transitions:
                if TransitionTypeEnum(tr.type) == TransitionTypeEnum.MAP_ACTION:
                    res.append(tr.cell)
        return res
    
    def findPath(
        self,
        start: MapPoint,
        end: MapPoint,
        allowDiag: bool = True,
        bAllowTroughEntity: bool = True,
        avoidObstacles: bool = True,
        forMapChange=False,
        mapChangeDirection=-1,
        cellsBlacklist=[],
    ) -> MovementPath:
        self.forMapChange = forMapChange
        self.mapChangeDirection = mapChangeDirection
        self.initAlgo(start, end, allowDiag, bAllowTroughEntity, avoidObstacles)
        open_list = []
        heapq.heappush(open_list, (0, start.cellId))
        while open_list:
            _, parentId = heapq.heappop(open_list)
            if parentId in self._isCellClosed:
                continue
            self._isCellClosed.add(parentId)
            for x, y in self.iterChilds(parentId):
                mp = MapPoint.fromCoords(x, y)
                moveCost = self.moveCost(x, y, parentId)
                cellId = mp.cellId
                if cellId in cellsBlacklist:
                    continue
                if self._allowTroughEntity:
                    distTmpToEnd = self.distFromEnd(mp.cellId)
                    if distTmpToEnd < self._distToEnd:
                        self._endCellAuxId = cellId
                        self._distToEnd = distTmpToEnd
                if cellId not in self._parentOfCell or moveCost < self._costOfCell[cellId]:
                    self._parentOfCell[cellId] = parentId
                    self._costOfCell[cellId] = moveCost
                    heuristic = self.HEURISTIC_SCALE * (abs(self._end.x - x) + abs(self._end.y - y))
                    totalCost = heuristic + moveCost
                    heapq.heappush(open_list, (totalCost, cellId))
        movPath = self.buildPath()
        return movPath

    def getMapPointWeight(self, x, y):
        cellId = MapTools.getCellIdByCoord(x, y)
        if cellId == self._end.cellId:
            return 1
        pointWeight = 0
        speed = self._mapData.getCellSpeed(cellId)
        entity_on_cell = self._isEntityOnCell.get(cellId)
        if self._allowTroughEntity:
            if entity_on_cell:
                pointWeight = 20
            elif speed >= 0:
                pointWeight = 6 - speed
            else:
                pointWeight = 12 + abs(speed)
        else:
            pointWeight = 1
            if entity_on_cell:
                pointWeight += 0.3
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                if MapTools.isValidCoord(x + dx, y + dy) and self._isEntityOnCell.get(
                    MapTools.getCellIdByCoord(x + dx, y + dy)
                ):
                    pointWeight += 0.3

            if self._mapData.pointSpecialEffects(x, y) & 2 == 2:
                pointWeight += 0.2
        return pointWeight
