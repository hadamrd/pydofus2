from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.TackleUtil import TackleUtil
from pydofus2.com.ankamagames.dofus.network.types.game.context.FightEntityDispositionInformations import (
    FightEntityDispositionInformations,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.Stat import Stat
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import EntitiesManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
    FightEntitiesFrame,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import (
    GameFightMonsterInformations,
)
from pydofus2.damageCalculation.tools.StatIds import StatIds
from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

logger = Logger("Dofus2")


class _ReachableCellData:
    STATE_UNDEFINED: int = 0
    STATE_REACHABLE: int = 1
    STATE_UNREACHABLE: int = 2
    STATE_WATCHED: int = 3
    mapPoint: MapPoint
    state: int
    evadePercent: float = 1
    bestRemainingMp: int = 0
    bestRemainingMpNoTackle: int = 0
    mpUpdated: bool = False
    gridX: int
    gridY: int
    cellGrid: list[list["_ReachableCellData"]]

    def __init__(
        self,
        mapPoint: MapPoint,
        gridX: int,
        gridY: int,
        cellGrid: list[list["_ReachableCellData"]],
    ):
        self.mapPoint = mapPoint
        self.gridX = gridX
        self.gridY = gridY
        self.cellGrid = cellGrid

    def findState(self) -> None:
        neighbour: _ReachableCellData = None
        cellData: Cell = MapDisplayManager().dataMap.cells[self.mapPoint.cellId]
        if not cellData.mov or cellData.nonWalkableDuringFight:
            self.state = self.STATE_UNREACHABLE

        else:
            self.evadePercent = 1
            if self.gridX > 0:
                neighbour = self.cellGrid[self.gridX - 1][self.gridY]
                if neighbour and neighbour.state == self.STATE_UNREACHABLE:
                    self.evadePercent *= neighbour.evadePercent

            if self.gridX < len(self.cellGrid) - 1:
                neighbour = self.cellGrid[self.gridX + 1][self.gridY]
                if neighbour and neighbour.state == self.STATE_UNREACHABLE:
                    self.evadePercent *= neighbour.evadePercent

            if self.gridY > 0:
                neighbour = self.cellGrid[self.gridX][self.gridY - 1]
                if neighbour and neighbour.state == self.STATE_UNREACHABLE:
                    self.evadePercent *= neighbour.evadePercent

            if self.gridY < len(self.cellGrid[0]) - 1:
                neighbour = self.cellGrid[self.gridX][self.gridY + 1]
                if neighbour and neighbour.state == self.STATE_UNREACHABLE:
                    self.evadePercent *= neighbour.evadePercent

            self.state = int(self.STATE_REACHABLE) if self.evadePercent == 1 else int(self.STATE_WATCHED)

    def updateMp(self, bestMp: int, bestUntackledMp: int) -> None:
        self.mpUpdated = True
        if bestMp > self.bestRemainingMp:
            self.bestRemainingMp = bestMp

        if bestUntackledMp > self.bestRemainingMpNoTackle:
            self.bestRemainingMpNoTackle = bestUntackledMp

    def __str__(self) -> str:
        return "Node " + self.mapPoint.cellId


class FightReachableCellsMaker:
    _cellGrid: list[list[_ReachableCellData]]
    _reachableCells: list[int]
    _unreachableCells: list[int]
    _mapPoint: MapPoint
    _mp: int
    _waitingCells: list[_ReachableCellData]
    _watchedCells: list[_ReachableCellData]

    def __init__(
        self,
        infos: GameFightMonsterInformations,
        fromCellId: int = -1,
        movementPoint: int = -1,
    ):
        entitiesFrame: FightEntitiesFrame = Kernel().worker.getFrame("FightEntitiesFrame")
        stats = StatsManager().getStats(infos.contextualId)
        movementPoints: Stat = stats.getStat(StatIds.MOVEMENT_POINTS)
        movementPointsValue: float = float(movementPoints.totalValue) if movementPoints is not None else float(0)
        self._reachableCells = list[int]()
        self._unreachableCells = list[int]()
        if movementPoint > -1:
            self._mp = movementPoint

        else:
            self._mp = int(movementPointsValue) if movementPointsValue > 0 else 0

        if fromCellId != -1:
            self._mapPoint = MapPoint.fromCellId(fromCellId)

        else:
            if infos.disposition.cellId == -1:
                logger.warn(
                    "Failed to initialize FightReachableCellsMaker for entity "
                    + infos.contextualId
                    + " because its cellId is -1"
                )
                return

            self._mapPoint = MapPoint.fromCellId(infos.disposition.cellId)

        self._cellGrid = list[list[_ReachableCellData]]([None] * (self._mp * 2 + 1))
        for i in range(len(self._cellGrid)):
            self._cellGrid[i] = list[_ReachableCellData]([None] * (self._mp * 2 + 1))

        entities = EntitiesManager().entities
        for entity in entities.values():
            if entity.id != infos.contextualId and entity.position:
                x = entity.position.x - self._mapPoint.x + self._mp
                y = entity.position.y - self._mapPoint.y + self._mp
                if x >= 0 and x < self._mp * 2 + 1 and y >= 0 and y < self._mp * 2 + 1:
                    entityInfos: GameFightFighterInformations = entitiesFrame.getEntityInfos(entity.id)
                    if entityInfos:
                        if not (
                            isinstance(
                                entityInfos.disposition,
                                FightEntityDispositionInformations,
                            )
                            and entityInfos.disposition.carryingCharacterId == infos.contextualId
                        ):
                            node = _ReachableCellData(entity.position, x, y, self._cellGrid)
                            node.state = _ReachableCellData.STATE_UNREACHABLE
                            evade = TackleUtil.getTackleForFighter(entityInfos, infos)
                            if not node.evadePercent or evade < node.evadePercent:
                                node.evadePercent = evade
                            self._cellGrid[x][y] = node

        self.compute()

    @property
    def reachableCells(self) -> list[int]:
        return self._reachableCells

    @property
    def unreachableCells(self) -> list[int]:
        return self._unreachableCells

    def compute(self) -> None:
        tmpCells: list[_ReachableCellData] = []
        node: _ReachableCellData = None
        mp: int = self._mp
        untacledMp: int = self._mp
        self._waitingCells = list[_ReachableCellData]()
        self._watchedCells = list[_ReachableCellData]()
        self.markNode(self._mapPoint.x, self._mapPoint.y, mp, untacledMp)
        while self._watchedCells or self._waitingCells:
            if self._waitingCells:
                tmpCells = self._waitingCells.copy()
                self._waitingCells.clear()
            else:
                tmpCells = self._watchedCells.copy()
                self._watchedCells.clear()

            for node in tmpCells:
                mp = int(node.bestRemainingMp * node.evadePercent + 0.49) - 1
                untacledMp = node.bestRemainingMpNoTackle - 1
                if MapPoint.isInMap(node.mapPoint.x - 1, node.mapPoint.y):
                    self.markNode(node.mapPoint.x - 1, node.mapPoint.y, mp, untacledMp)

                if MapPoint.isInMap(node.mapPoint.x + 1, node.mapPoint.y):
                    self.markNode(node.mapPoint.x + 1, node.mapPoint.y, mp, untacledMp)

                if MapPoint.isInMap(node.mapPoint.x, node.mapPoint.y - 1):
                    self.markNode(node.mapPoint.x, node.mapPoint.y - 1, mp, untacledMp)

                if MapPoint.isInMap(node.mapPoint.x, node.mapPoint.y + 1):
                    self.markNode(node.mapPoint.x, node.mapPoint.y + 1, mp, untacledMp)

    def markNode(self, x: int, y: int, mp: int, untackledMp: int) -> None:
        xTab: int = x - self._mapPoint.x + self._mp
        yTab: int = y - self._mapPoint.y + self._mp
        node: _ReachableCellData = self._cellGrid[xTab][yTab]
        if not node:
            node = _ReachableCellData(MapPoint.fromCoords(x, y), xTab, yTab, self._cellGrid)
            self._cellGrid[xTab][yTab] = node
            node.findState()
            if node.state != _ReachableCellData.STATE_UNREACHABLE:
                if mp >= 0:
                    self._reachableCells.append(node.mapPoint.cellId)
                else:
                    self._unreachableCells.append(node.mapPoint.cellId)
        if node.state == _ReachableCellData.STATE_UNREACHABLE and (self._mapPoint.x != x or self._mapPoint.y != y):
            return

        if not node.mpUpdated or mp > node.bestRemainingMp or untackledMp > node.bestRemainingMpNoTackle:
            if mp >= 0 and node.mapPoint.cellId in self._unreachableCells:
                self._reachableCells.append(node.mapPoint.cellId)
                self._unreachableCells.remove(node.mapPoint.cellId)

            node.updateMp(mp, untackledMp)
            if untackledMp > 0:
                if (
                    node.state == _ReachableCellData.STATE_REACHABLE
                    or node.mapPoint.cellId == self._mapPoint.cellId
                    and node.state == _ReachableCellData.STATE_UNREACHABLE
                ):
                    self._waitingCells.append(node)

                elif node.state == _ReachableCellData.STATE_WATCHED:
                    self._watchedCells.append(node)
