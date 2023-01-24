import math
from pydofus2.com.ankamagames.atouin.messages.CellClickMessage import CellClickMessage
from pydofus2.com.ankamagames.atouin.messages.EntityMovementCompleteMessage import (
    EntityMovementCompleteMessage,
)
from pydofus2.com.ankamagames.atouin.messages.MapContainerRollOutMessage import (
    MapContainerRollOutMessage,
)
from pydofus2.com.ankamagames.atouin.types.Selection import Selection
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStats import EntityStats
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.MapMovementAdapter import (
    MapMovementAdapter,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightSpellCastAction import (
    GameFightSpellCastAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightTurnFinishAction import (
    GameFightTurnFinishAction,
)
from typing import TYPE_CHECKING
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementMessage import GameMapMovementMessage


if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import (
        FightContextFrame,
    )
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
    CurrentPlayedFighterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.FightReachableCellsMaker import (
    FightReachableCellsMaker,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.TackleUtil import TackleUtil
from pydofus2.com.ankamagames.dofus.network.enums.ChatActivableChannelsEnum import (
    ChatActivableChannelsEnum,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.chat.ChatClientMultiMessage import (
    ChatClientMultiMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementRequestMessage import (
    GameMapMovementRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapNoMovementMessage import (
    GameMapNoMovementMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.ShowCellRequestMessage import (
    ShowCellRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnFinishMessage import (
    GameFightTurnFinishMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnReadyRequestMessage import (
    GameFightTurnReadyRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.pathfinding.Pathfinding import Pathfinding
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.positions.MovementPath import MovementPath
from pydofus2.com.ankamagames.jerakine.types.positions.PathElement import PathElement
from pydofus2.damageCalculation.tools.StatIds import StatIds
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from typing import TYPE_CHECKING
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
    FightEntitiesFrame,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightBattleFrame import (
        FightBattleFrame,
    )
    from pydofus2.com.ankamagames.jerakine.entities.interfaces.IMovable import IMovable
logger = Logger("Dofus2")


class FightTurnFrame(Frame):

    TAKLED_CURSOR_NAME: str = "TackledCursor"

    SELECTION_PATH: str = "FightMovementPath"

    SELECTION_END_PATH: str = "FightMovementEndPath"

    SELECTION_PATH_TACKLED: str = "FightMovementPathTackled"

    SELECTION_PATH_UNREACHABLE: str = "FightMovementPathUnreachable"

    SELECTION_MOVEMENT_AREA: str = "FightMovementArea"

    REMIND_TURN_DELAY: int = 15

    _movementSelection: Selection = None

    _movementTargetSelection: Selection = None

    _movementSelectionTackled: Selection = None

    _movementSelectionUnreachable: Selection = None

    _movementAreaSelection: Selection = None

    _isRequestingMovement: bool = None

    _spellCastFrame: Frame = None

    _finishingTurn: bool = None

    _remindTurnTimeoutId: BenchmarkTimer = None

    _myTurn: bool = None

    _turnDuration: int = None

    _remainingDurationSeconds: int = None

    _lastCell: MapPoint = None

    _cells: list[int] = None

    _cellsTackled: list[int] = None

    _cellsUnreachable: list[int] = None

    _lastPath: MovementPath = None

    _intervalTurn: BenchmarkTimer = None

    _playerEntity: IEntity = None

    _currentFighterId: float = None

    _tackleByCellId: dict = None

    _turnFinishingNoNeedToRedrawMovement: bool = False

    _lastMP: int = 0

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.HIGH

    @property
    def playerEntity(self) -> IEntity:
        self._currentFighterId = CurrentPlayedFighterManager().currentFighterId
        return DofusEntities.getEntity(self._currentFighterId)

    @property
    def myTurn(self) -> bool:
        return self._myTurn

    @myTurn.setter
    def myTurn(self, b: bool) -> None:
        self._finishingTurn = False
        self._currentFighterId = CurrentPlayedFighterManager().currentFighterId
        self._playerEntity = DofusEntities.getEntity(self._currentFighterId)
        self._turnFinishingNoNeedToRedrawMovement = False
        self._myTurn = b
        if b:
            pass
        else:
            self._isRequestingMovement = False
            if self._remindTurnTimeoutId is not None:
                self._remindTurnTimeoutId.cancel()

    @property
    def turnDuration(self) -> int:
        return self._turnDuration

    @turnDuration.setter
    def turnDuration(self, v: int) -> None:
        self._turnDuration = v
        self._remainingDurationSeconds = math.floor(v)
        if self._intervalTurn:
            self._intervalTurn.cancel()
        self._intervalTurn = BenchmarkTimer(10, self.onSecondTick)

    @property
    def lastPath(self) -> MovementPath:
        return self._lastPath

    @property
    def movementAreaSelection(self) -> Selection:
        return self._movementAreaSelection

    def freePlayer(self) -> None:
        self._isRequestingMovement = False

    def pushed(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameFightSpellCastAction):
            gfsca = msg
            if self._spellCastFrame is not None:
                Kernel().worker.removeFrame(self._spellCastFrame)
            self.removePath()
            if self._myTurn:
                self.startRemindTurn()
            bf: "FightBattleFrame" = Kernel().worker.getFrame("FightBattleFrame")
            playerInformation: "GameFightFighterInformations" = FightEntitiesFrame.getCurrentInstance().getEntityInfos(
                self._currentFighterId
            )
            if bf and bf.turnsCount <= 1 or playerInformation and playerInformation.spawnInfo.alive:
                import pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightSpellCastFrame as fscf

                self._spellCastFrame = fscf.FightSpellCastFrame(gfsca.spellId)
                Kernel().worker.addFrame(self._spellCastFrame)
            return True

        elif isinstance(msg, CellClickMessage):
            ccmsg = msg
            if not self.myTurn:
                return False
            self.askMoveTo(ccmsg.cell)
            return True

        elif isinstance(msg, GameMapNoMovementMessage):
            if not self.myTurn:
                return False
            self._isRequestingMovement = False
            self.removePath()
            return False

        elif isinstance(msg, EntityMovementCompleteMessage):
            emcmsg = msg
            if not self.myTurn:
                return True
            if float(emcmsg.entity.id) == float(self._currentFighterId):
                self._isRequestingMovement = False
                if self._finishingTurn:
                    self.finishTurn()
            return True

        if isinstance(msg, GameFightTurnFinishAction):
            if not self.myTurn:
                return False
            self._turnFinishingNoNeedToRedrawMovement = True
            entitiesFrame: "FightEntitiesFrame" = Kernel().worker.getFrame("FightEntitiesFrame")
            playerInfos: "GameFightFighterInformations" = entitiesFrame.getEntityInfos(self._currentFighterId)
            if self._remainingDurationSeconds > 0 and not playerInfos.stats.summoned:
                basicTurnDuration = CurrentPlayedFighterManager().getBasicTurnDuration()
                secondsToReport = math.floor(self._remainingDurationSeconds / 2)
                if basicTurnDuration + secondsToReport > 60:
                    secondsToReport = 60 - basicTurnDuration
                if secondsToReport > 0:
                    Logger.debug(
                        I18n.getUiText("ui.fight.secondsAdded", [secondsToReport]),
                        "n",
                        secondsToReport <= 1,
                        secondsToReport == 0,
                    )
                self._remainingDurationSeconds = 0
                self._intervalTurn = 0
            imE: "IMovable" = DofusEntities.getEntity(self._currentFighterId)
            if not imE:
                return True
            if imE.isMoving:
                self._finishingTurn = True
            else:
                self.finishTurn()
            return True

        if isinstance(msg, MapContainerRollOutMessage):
            self.removePath()
            return True

        if isinstance(msg, GameFightTurnReadyRequestMessage):
            self._turnFinishingNoNeedToRedrawMovement = True
            return False

        if isinstance(msg, GameMapMovementMessage):
            self._isRequestingMovement = False
            return False
        else:
            return False

    def pulled(self) -> bool:
        if self._remindTurnTimeoutId:
            self._remindTurnTimeoutId.cancel()
        if self._intervalTurn:
            self._intervalTurn.cancel()
        self.removePath()
        self.removeMovementArea()
        Kernel().worker.removeFrame(self._spellCastFrame)
        return True

    def drawMovementArea(self) -> list[int]:
        # logger.debug("drawing the movement area")
        if not self.playerEntity or self.playerEntity.isMoving:
            logger.debug(f"player {self.playerEntity} is moving {self.playerEntity.isMoving} or not found")
            self.removeMovementArea()
            return []
        playerPosition: MapPoint = self.playerEntity.position
        stats: EntityStats = CurrentPlayedFighterManager().getStats()
        if not stats:
            logger.debug("no stats")
            return
        movementPoints: int = stats.getStatTotalValue(StatIds.MOVEMENT_POINTS)
        # logger.debug(f"movementPoints available {movementPoints}")
        self._lastMP = movementPoints
        entitiesFrame: FightEntitiesFrame = FightEntitiesFrame.getCurrentInstance()
        playerInfos: GameFightFighterInformations = entitiesFrame.getEntityInfos(self.playerEntity.id)
        tackle: float = TackleUtil.getTackle(playerInfos, playerPosition)
        self._tackleByCellId = dict()
        self._tackleByCellId[playerPosition.cellId] = tackle
        mpLost: int = int(movementPoints * (1 - tackle) + 0.5)
        if mpLost < 0:
            mpLost = 0
        movementPoints -= mpLost
        if movementPoints == 0:
            self.removeMovementArea()
            return []
        fightReachableCellsMaker: FightReachableCellsMaker = FightReachableCellsMaker(playerInfos)
        reachableCells: list[int] = fightReachableCellsMaker.reachableCells
        if len(reachableCells) == 0:
            self.removeMovementArea()
            return []
        return reachableCells

    @property
    def currentPosition(self) -> MapPoint:
        playerInfos: GameFightFighterInformations = FightEntitiesFrame.getCurrentInstance().getEntityInfos(
            self.playerEntity.id
        )
        currentMp = MapPoint.fromCellId(playerInfos.disposition.cellId)
        return currentMp

    def drawPath(self, destCell: MapPoint = None) -> None:
        firstObstacle: PathElement = None
        self._cells = []
        self._cellsTackled = []
        self._cellsUnreachable = []
        # logger.debug(f"Drawing the move path to {destCell}")
        if Kernel().worker.contains("FightSpellCastFrame"):
            return
        fcf: "FightContextFrame" = Kernel().worker.getFrame("FightContextFrame")
        if self._isRequestingMovement:
            logger.debug("Already requesting movement abort")
            return
        if not destCell:
            if fcf.currentCell == -1:
                # logger.debug("No current cell hovered to draw path")
                return
            destCell = MapPoint.fromCellId(fcf.currentCell)
        if not self.playerEntity:
            logger.debug("No player entity found")
            self.removePath()
            return
        stats: EntityStats = CurrentPlayedFighterManager().getStats()
        mpLost: int = 0
        apLost: int = 0
        movementPoints: int = stats.getStatTotalValue(StatIds.MOVEMENT_POINTS)
        actionPoints: int = stats.getStatTotalValue(StatIds.ACTION_POINTS)
        logger.debug(f"MP : {movementPoints}, AP : {actionPoints}")

        if self.playerEntity.isMoving or self.currentPosition.distanceToCell(destCell) > movementPoints:
            logger.debug(
                f"Player is moving {self.playerEntity.isMoving} or dest is too far {self.currentPosition.distanceToCell(destCell)} from {movementPoints} abort"
            )
            self.removePath()
            return
        path: MovementPath = Pathfinding.findPath(
            DataMapProvider(), self.currentPosition, destCell, False, False, True
        )
        logger.debug(f"Found a path {path}")
        if len(DataMapProvider().obstaclesCells) > 0 and (len(path.path) == 0 or len(path.path) > movementPoints):
            logger.debug("Path is empty because of obstacles or too long for the available move points")
            path = Pathfinding.findPath(
                DataMapProvider(),
                self.playerEntity.position,
                destCell,
                False,
                False,
                False,
            )
            logger.debug(f"Path found {path}")
            if len(path.path) > 0:
                pathLen = len(path.path)
                for i in range(pathLen):
                    if path.path[i].cellId in DataMapProvider().obstaclesCells:
                        firstObstacle = path.path[i]
                        for j in range(pathLen):
                            self._cellsUnreachable.append(path.path[j].cellId)
                        self._cellsUnreachable.append(path.end.cellId)
                        path.end = firstObstacle.step
                        path.path = path.path[:i]
                        break
        if len(path.path) == 0 or len(path.path) > movementPoints:
            logger.debug(f"Path found empty {len(path.path)} or too long compared to mp {movementPoints}")
            self.removePath()
            return
        self._lastPath = path
        isFirst: bool = True
        mpCount: int = 0
        apLost = 0
        lastPe: PathElement = None
        entitiesFrame: "FightEntitiesFrame" = Kernel().worker.getFrame("FightEntitiesFrame")
        playerInfos: GameFightFighterInformations = entitiesFrame.getEntityInfos(self.playerEntity.id)
        for pe in path.path:
            if isFirst:
                isFirst = False
            else:
                tackle = TackleUtil.getTackle(playerInfos, lastPe.step)
                mpLost += int((movementPoints - mpCount) * (1 - tackle) + 0.5)
                if mpLost < 0:
                    mpLost = 0
                apLost += int(actionPoints * (1 - tackle) + 0.5)
                if apLost < 0:
                    apLost = 0
                movementPoints = stats.getStatTotalValue(StatIds.MOVEMENT_POINTS) - mpLost
                actionPoints = stats.getStatTotalValue(StatIds.ACTION_POINTS) - apLost
                if mpCount < movementPoints:
                    if mpLost > 0:
                        self._cellsTackled.append(pe.step.cellId)
                    else:
                        self._cells.append(pe.step.cellId)
                    mpCount += 1
                else:
                    self._cellsUnreachable.append(pe.step.cellId)
            lastPe = pe

        tackle = TackleUtil.getTackle(playerInfos, lastPe.step)
        mpLost += int((movementPoints - mpCount) * (1 - tackle) + 0.5)
        if mpLost < 0:
            mpLost = 0
        apLost += int(actionPoints * (1 - tackle) + 0.5)
        if apLost < 0:
            apLost = 0
        movementPoints = stats.getStatTotalValue(StatIds.MOVEMENT_POINTS) - mpLost
        if mpCount < movementPoints:
            if firstObstacle:
                movementPoints = len(path.path)
            if mpLost > 0:
                self._cellsTackled.append(path.end.cellId)
            else:
                self._cells.append(path.end.cellId)
        elif firstObstacle:
            self._cellsUnreachable.insert(0, path.end.cellId)
            movementPoints = len(path.path) - 1
        else:
            self._cellsUnreachable.append(path.end.cellId)

        logger.debug(
            f"cells : {self._cells}, cellsTackled : {self._cellsTackled}, cellsUnreachable : {self._cellsUnreachable}"
        )

    def updatePath(self) -> None:
        self.drawPath(self._lastCell)

    def removePath(self) -> None:
        self._movementSelection = None
        self._movementSelectionTackled = None
        self._movementSelectionUnreachable = None
        self._movementTargetSelection = None
        self._lastPath = None
        self._cells = None

    def removeMovementArea(self) -> None:
        self._movementAreaSelection = None

    def askMoveTo(self, cells: list[int] = [], cellsTackled: list[int] = []) -> bool:
        if self._isRequestingMovement:
            logger.warn("Already requesting movement")
            return False
        self._isRequestingMovement = True
        if not self.playerEntity:
            logger.warn("The player tried to move before its character was added to the scene. Aborting.")
            self._isRequestingMovement = False
            return False
        if self.playerEntity.isMoving:
            logger.warn("The player is already moving")
            self._isRequestingMovement = False
            return False
        if cells:
            self._cells = cells
        if cellsTackled:
            self._cellsTackled = cellsTackled
        if (self._cells is None or len(self._cells) == 0) and (
            self._cellsTackled is None or len(self._cellsTackled) == 0
        ):
            logger.debug(f"No cells to move to {self._cells} {self._cellsTackled}")
            self._isRequestingMovement = False
            return False
        path: MovementPath = MovementPath()
        cells: list[int] = self._cells if (self._cells and len(self._cells) > 0) else self._cellsTackled
        cells.insert(0, self.currentPosition.cellId)
        path.fillFromCellIds(cells[0:-1])
        path.end = MapPoint.fromCellId(cells[-1])
        path.path[-1].orientation = path.path[-1].step.orientationTo(path.end)
        fightBattleFrame: "FightBattleFrame" = Kernel().worker.getFrame("FightBattleFrame")
        if not fightBattleFrame or not fightBattleFrame.fightIsPaused:
            gmmrmsg = GameMapMovementRequestMessage()
            keyMovements = MapMovementAdapter.getServerMovement(path)
            currMapId = PlayedCharacterManager().currentMap.mapId
            gmmrmsg.init(keyMovements, currMapId)
            ConnectionsHandler()._conn.send(gmmrmsg)
            logger.debug(f"Sent movement request {keyMovements}")
        else:
            logger.debug("Fight is not paused, and battle frame is running can't move")
            self._isRequestingMovement = False
        self.removePath()
        return True

    def finishTurn(self) -> None:
        gftfmsg: GameFightTurnFinishMessage = GameFightTurnFinishMessage()
        gftfmsg.init(False)
        ConnectionsHandler()._conn.send(gftfmsg)
        self.removeMovementArea()
        self._finishingTurn = False

    def onSecondTick(self) -> None:
        if self._remainingDurationSeconds > 0:
            self._remainingDurationSeconds -= 1
        else:
            self._intervalTurn.cancel()

    def showCell(self, cellId: MapPoint) -> None:
        if not Kernel().worker.contains("FightSpellCastFrame"):
            if DataMapProvider().pointMov(
                MapPoint.fromCellId(cellId).x,
                MapPoint.fromCellId(cellId).y,
                True,
            ):
                scrmsg = ShowCellRequestMessage()
                scrmsg.init(cellId)
                ConnectionsHandler()._conn.send(scrmsg)
                text = I18n.getUiText(
                    "ui.fightAutomsg.cell",
                    ["{cell," + str(cellId) + "::" + str(cellId) + "}"],
                )
                ccmmsg = ChatClientMultiMessage()
                ccmmsg.init(content_=text, channel_=ChatActivableChannelsEnum.CHANNEL_TEAM)
                ConnectionsHandler()._conn.send(ccmmsg)
