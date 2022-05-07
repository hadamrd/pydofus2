import collections
import math
import random
from com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from time import sleep
from types import FunctionType
from com.ankamagames.atouin.AtouinConstants import AtouinConstants
from com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from com.ankamagames.dofus.internalDatacenter.stats.EntityStats import EntityStats
from com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import CurrentPlayedFighterManager
from com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightNoSpellCastMessage import (
    GameActionFightNoSpellCastMessage,
)
from com.ankamagames.dofus.network.messages.game.actions.sequence.SequenceEndMessage import SequenceEndMessage
from com.ankamagames.dofus.network.messages.game.actions.sequence.SequenceStartMessage import SequenceStartMessage
from com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import GameContextActorInformations
from com.ankamagames.jerakine.logger.Logger import Logger
from com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from com.ankamagames.atouin.messages.CellClickMessage import CellClickMessage
from com.ankamagames.atouin.messages.MapLoadedMessage import MapLoadedMessage
from com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from com.ankamagames.dofus.kernel.Kernel import Kernel
from com.ankamagames.dofus.kernel.net.ConnectionType import ConnectionType
from com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
    FightEntitiesFrame,
)
from com.ankamagames.dofus.logic.game.fight.miscs.FightReachableCellsMaker import (
    FightReachableCellsMaker,
)
from com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayEntitiesFrame import (
    RoleplayEntitiesFrame,
)
from com.ankamagames.dofus.network.messages.common.basic.BasicPingMessage import (
    BasicPingMessage,
)
from com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightCastRequestMessage import (
    GameActionFightCastRequestMessage,
)
from com.ankamagames.dofus.network.messages.game.context.fight.GameFightEndMessage import (
    GameFightEndMessage,
)
from com.ankamagames.dofus.network.messages.game.context.fight.GameFightJoinMessage import (
    GameFightJoinMessage,
)
from com.ankamagames.dofus.network.messages.game.context.fight.GameFightReadyMessage import (
    GameFightReadyMessage,
)
from com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnFinishMessage import (
    GameFightTurnFinishMessage,
)
from com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnStartMessage import (
    GameFightTurnStartMessage,
)
from com.ankamagames.dofus.network.messages.game.context.fight.character.GameFightShowFighterMessage import (
    GameFightShowFighterMessage,
)
from com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataMessage import (
    MapComplementaryInformationsDataMessage,
)
from com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import (
    GameFightMonsterInformations,
)
from com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayGroupMonsterInformations import (
    GameRolePlayGroupMonsterInformations,
)
from com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from com.ankamagames.jerakine.entities.interfaces.IInteractive import IInteractive
from com.ankamagames.jerakine.map.LosDetector import LosDetector
from com.ankamagames.jerakine.messages.Frame import Frame
from com.ankamagames.jerakine.messages.Message import Message
from com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from com.ankamagames.jerakine.types.enums.Priority import Priority
from com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from typing import TYPE_CHECKING, Tuple
from com.ankamagames.jerakine.types.zones.Cross import Cross
from com.ankamagames.jerakine.types.zones.IZone import IZone
from com.ankamagames.jerakine.types.zones.Lozenge import Lozenge
from com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum
from damageCalculation.tools import StatIds


if TYPE_CHECKING:
    from com.ankamagames.dofus.logic.game.fight.frames.FightTurnFrame import (
        FightTurnFrame,
    )
    from com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import (
        FightContextFrame,
    )
    from com.ankamagames.dofus.logic.game.fight.frames.FightBattleFrame import FightBattleFrame
    from com.ankamagames.dofus.logic.game.fight.frames.FightSpellCastFrame import FightSpellCastFrame


logger = Logger("Dofus2")


class _Target:
    def __init__(self, entityId: float, pos: MapPoint) -> None:
        self.pos: MapPoint = pos
        self.entityId = entityId

    def __str__(self) -> str:
        return f"({self.entityId} at {self.pos.cellId})"


class BotFightFrame(Frame, metaclass=Singleton):

    _frameFightListRequest: bool

    _fightCount: int = 0

    _mapPos: list

    _enabled: bool

    _inFight: bool

    _lastEntityOver: IInteractive

    _wait: bool

    _turnPlayed: int

    _myTurn: bool

    _turnAction: list[FunctionType]

    _spellId = 13516  # Sadida ronce

    _lastTarget: int = None

    _spellw: SpellWrapper = None

    def __init__(self):
        self._turnAction = []
        self._spellw = None
        super().__init__()

    def pushed(self) -> bool:
        self._enabled = True
        self.fakeActivity()
        self._myTurn = False
        self._wantcastSpell = None
        self._reachableCells = None
        self._turnAction = []
        self._seqQueue = []
        self._waitingSeqEnd = False
        self._turnPlayed = 0
        self._spellw = None
        self._actionTimeout = None
        return True

    @property
    def turnFrame(self) -> "FightTurnFrame":
        return Kernel().getWorker().getFrame("FightTurnFrame")

    @property
    def fightContextFrame(self) -> "FightContextFrame":
        return Kernel().getWorker().getFrame("FightContextFrame")

    @property
    def entitiesFrame(self) -> "FightEntitiesFrame":
        return Kernel().getWorker().getFrame("FightEntitiesFrame")

    @property
    def spellFrame(self) -> "FightSpellCastFrame":
        return Kernel().getWorker().getFrame("FightSpellCastFrame")

    @property
    def battleFrame(self) -> "FightBattleFrame":
        return Kernel().getWorker().getFrame("FightBattleFrame")

    def pulled(self) -> bool:
        self._enabled = False
        return True

    @property
    def priority(self) -> int:
        return Priority.VERY_LOW

    @property
    def fightCount(self) -> int:
        return self._fightCount

    def findPathToTarget(self, spellw: SpellWrapper, targets: list[_Target]) -> Tuple[_Target, list[int]]:
        """
        Find path to the closest ldv to hit a mob.
        :param origin: position of the character
        :param po: max range of the spell
        :param targets: positions of the mobs
        :return: cell of the mob, path to the ldv if any else None
        """
        if not targets:
            logger.debug("[FightAlgo] Not hittable target found")
            return None, None
        spellZone = self.getSpellZone(spellw)
        origin = self.fighterPos
        logger.debug(f"[FightAlgo] Searching for path to hit some target, origin = {origin.cellId}")
        queue = collections.deque([[origin.cellId]])
        seen = {origin.cellId}
        while queue:
            path = queue.popleft()
            currCellId: int = path[-1]
            currSpellZone = spellZone.getCells(currCellId)
            ldv = set(LosDetector.getCell(DataMapProvider(), currSpellZone, MapPoint.fromCellId(currCellId)))
            for target in targets:
                if target.pos.cellId in ldv:
                    logger.debug(f"[FightAlgo] Found path {path} to hit a target {target}")
                    return target, path[1:]
            currReachableCells = set(FightReachableCellsMaker(self.fighterInfos, currCellId, 1).reachableCells)
            for cellId in currReachableCells:
                if cellId not in seen:
                    queue.append(path + [cellId])
                    seen.add(cellId)
        logger.debug(f"[FightAlgo] No valid path to reach a target found")
        return None, None

    def playTurn(self):
        targets = self.getTargetableEntities(self.spellw, targetSum=False)
        if not targets:
            targets = self.getTargetableEntities(self.spellw, targetSum=True)
            if not targets:
                self.addTurnAction(self.turnEnd, [])
                self.nextTurnAction()
                return
        logger.info(f"[FightAlgo] MP : {self.movementPoints}, AP : {self.actionPoints}")
        logger.info(f"[FightAlgo] Current atack spell : {self.spellw.spell.name}")
        self.updateReachableCells()
        logger.info(f"[FightAlgo] Current reachable cells {self._reachableCells}")
        target, path = self.findPathToTarget(self.spellw, targets)
        if target is not None:
            if len(path) == 0:
                logger.debug(f"[FightAlgo] Can hit target {target} from current position")
                self.addTurnAction(self.castSpell, [self._spellId, target.pos.cellId])
            elif path[-1] in self._reachableCells:
                logger.debug(
                    f"[FightAlgo] Last Path cell to target {target} is reachable will move to it before casting the spell"
                )
                self.addTurnAction(self.askMove, [path])
                self.addTurnAction(self.castSpell, [self._spellId, target.pos.cellId])
            else:
                found = False
                for i, cellId in enumerate(path):
                    if cellId not in self._reachableCells:
                        if i != 0:
                            found = True
                            self.addTurnAction(self.askMove, [path[:i]])
                        break
                logger.debug(f"[FightAlgo] Have enough PM to get closer to the target ? {found}")
                self.addTurnAction(self.turnEnd, [])
        else:
            logger.warn("[FightAlgo] No path to any target found")
            self.addTurnAction(self.turnEnd, [])
        self.nextTurnAction()

    @property
    def spellw(self) -> SpellWrapper:
        if self._spellw is None:
            for spellw in PlayedCharacterManager().playerSpellList:
                if spellw.id == self._spellId:
                    self._spellw = spellw
        return self._spellw

    def getActualSpellRange(self, spellw: SpellWrapper) -> int:
        playerStats: EntityStats = CurrentPlayedFighterManager().getStats()
        range: int = spellw.maximalRangeWithBoosts
        minRange: int = spellw.minimalRange
        if spellw["rangeCanBeBoosted"]:
            range += playerStats.getStatTotalValue(StatIds.RANGE) - playerStats.getStatAdditionalValue(StatIds.RANGE)
        if range < minRange:
            range = minRange
        range = min(range, AtouinConstants.MAP_WIDTH * AtouinConstants.MAP_HEIGHT)
        if range < 0:
            range = 0
        return range

    def getSpellShape(self, spellw: SpellWrapper) -> int:
        spellShape: int = 0
        spellEffect: EffectInstance = None
        for spellEffect in spellw["effects"]:
            if spellEffect.zoneShape != 0 and (
                spellEffect.zoneSize > 0
                or spellEffect.zoneSize == 0
                and (spellEffect.zoneShape == SpellShapeEnum.P or spellEffect.zoneMinSize < 0)
            ):
                spellShape = spellEffect.zoneShape
        return spellShape

    def getSpellZone(self, spellw: SpellWrapper) -> IZone:
        range: int = self.getActualSpellRange(spellw)
        minRange: int = spellw.minimalRange
        spellShape: int = self.getSpellShape(spellw)
        castInLine: bool = spellw["castInLine"] or spellShape == SpellShapeEnum.l
        if castInLine and spellw["castInDiagonal"]:
            shapePlus = Cross(minRange, range, DataMapProvider())
            shapePlus.allDirections = True
            return shapePlus
        elif castInLine:
            return Cross(minRange, range, DataMapProvider())
        elif spellw["castInDiagonal"]:
            shapePlus = Cross(minRange, range, DataMapProvider())
            shapePlus.diagonal = True
            return shapePlus
        else:
            return Lozenge(minRange, range, DataMapProvider())

    def addTurnAction(self, fct: FunctionType, args: list) -> None:
        self._turnAction.append({"fct": fct, "args": args})

    def nextTurnAction(self) -> None:
        battleSeqStack = self.battleFrame.getSequencesStack()
        if len(battleSeqStack) > 0:
            logger.warn(f"[FightBot] Battle is busy processing sequences stack of size {len(battleSeqStack)}")
            BenchmarkTimer(0.1, self.nextTurnAction).start()
        else:
            logger.debug(f"[FightBot] Next turn actions, {[a['fct'].__name__ for a in self._turnAction]}")
            if len(self._turnAction) > 0:
                action = self._turnAction.pop(0)
                action["fct"](*action["args"])
                self._actionTimeout = BenchmarkTimer(3, action["fct"], action["args"])
                self._actionTimeout.start()
                self._waitingSeqEnd = True
            else:
                self.playTurn()

    def updateReachableCells(self) -> None:
        self._reachableCells = FightReachableCellsMaker(self.fighterInfos).reachableCells

    def canCastSpell(self, spellw: SpellWrapper, targetId: int) -> bool:
        reason = [""]
        if CurrentPlayedFighterManager().canCastThisSpell(self._spellId, spellw.spellLevel, targetId, reason):
            return True
        else:
            logger.error(f"[FightBot] Unable to cast spell for reason {reason[0]}")
            return False

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameFightJoinMessage):
            self._fightCount += 1
            self._inFight = True
            return False

        elif isinstance(msg, GameFightEndMessage):
            self._inFight = False
            return True

        elif isinstance(msg, GameActionFightNoSpellCastMessage):
            logger.debug(f"[FightBot] Failed to cast spell")
            self.turnEnd()
            return True

        elif isinstance(msg, MapComplementaryInformationsDataMessage):
            self._wait = False
            return False

        elif isinstance(msg, MapLoadedMessage):
            self._wait = True
            return False

        elif isinstance(msg, GameFightShowFighterMessage):
            self._turnPlayed = 0
            self._myTurn = False
            startFightMsg = GameFightReadyMessage()
            startFightMsg.init(True)
            ConnectionsHandler.getConnection().send(startFightMsg)
            return True

        elif isinstance(msg, SequenceEndMessage):
            if self._myTurn:
                if self._seqQueue:
                    self._seqQueue.pop()
                    if not self._seqQueue:
                        if self._waitingSeqEnd:
                            self._waitingSeqEnd = False
                            self._actionTimeout.cancel()
                            self.nextTurnAction()
            return True

        elif isinstance(msg, SequenceStartMessage):
            if self._myTurn:
                self._seqQueue.append(msg)
            return True

        elif isinstance(msg, GameFightTurnStartMessage):
            turnStartMsg = msg
            self._myTurn = int(turnStartMsg.id) == int(PlayedCharacterManager().id)
            if self._myTurn:
                logger.debug("my turn to play")
                self._seqQueue.clear()
                self._myTurn = True
                self._turnAction.clear()
                self._turnPlayed += 1
                self.nextTurnAction()

        return False

    @property
    def actionPoints(self) -> int:
        stats = CurrentPlayedFighterManager().getStats()
        return stats.getStatTotalValue(StatIds.ACTION_POINTS)

    @property
    def movementPoints(self) -> int:
        stats = CurrentPlayedFighterManager().getStats()
        return stats.getStatTotalValue(StatIds.MOVEMENT_POINTS)

    def turnEnd(self) -> None:
        self._myTurn = False
        self._seqQueue.clear()
        self._turnAction.clear()
        if self.turnFrame:
            self.turnFrame.finishTurn()

    def fakeActivity(self) -> None:
        if not self._enabled:
            return
        BenchmarkTimer(60 * 5, self.fakeActivity).start()
        bpmgs: BasicPingMessage = BasicPingMessage()
        bpmgs.init(False)
        ConnectionsHandler.getConnection().send(bpmgs, ConnectionType.TO_ALL_SERVERS)

    @property
    def fighterInfos(self) -> "GameContextActorInformations":
        info = self.entitiesFrame.getEntityInfos(CurrentPlayedFighterManager().currentFighterId)
        return info

    @property
    def fighterPos(self) -> "MapPoint":
        return MapPoint.fromCellId(self.fighterInfos.disposition.cellId)

    def getTargetableEntities(self, spellw: SpellWrapper, targetSum=False) -> list[_Target]:
        result = list[_Target]()
        logger.debug(f"Deads list : {self.battleFrame._deadTurnsList}")
        for entity in FightEntitiesFrame.getCurrentInstance().entities.values():
            if entity.contextualId < 0 and isinstance(entity, GameFightMonsterInformations):
                monster = entity
                if (
                    monster.spawnInfo.teamId != self.fighterInfos.spawnInfo.teamId
                    and float(entity.contextualId) not in self.battleFrame._deadTurnsList
                    and (targetSum or not monster.stats.summoned)
                    and self.canCastSpell(spellw, entity.contextualId)
                ):
                    result.append(_Target(entity.contextualId, MapPoint.fromCellId(entity.disposition.cellId)))
        logger.debug(f"[FightBot] Found targets : {[str(tgt) for tgt in result]}")
        return result

    def castSpell(self, spellId: int, cellId: bool) -> None:
        logger.debug(f"Casting spell {spellId} on cell {cellId}")
        gafcrmsg: GameActionFightCastRequestMessage = GameActionFightCastRequestMessage()
        gafcrmsg.init(spellId, cellId)
        ConnectionsHandler.getConnection().send(gafcrmsg)

    def askMove(self, cells: list[int], cellsTackled: list[int] = []) -> None:
        logger.debug(f"[FightBot] Ask move follwing path {cells}")
        if not self._myTurn:
            logger.warn("[FightBot] Wants to move when it's not its turn yet")
            return False
        fightTurnFrame: "FightTurnFrame" = Kernel().getWorker().getFrame("FightTurnFrame")
        if not fightTurnFrame:
            logger.warn("[FightBot] Wants to move inside fight but 'FightTurnFrame' not found in kernel")
            return False
        fightTurnFrame.askMoveTo(cells, cellsTackled)
        return True
