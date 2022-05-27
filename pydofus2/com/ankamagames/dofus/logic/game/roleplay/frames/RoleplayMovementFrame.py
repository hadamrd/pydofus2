from threading import Timer
from time import perf_counter, sleep
from typing import TYPE_CHECKING
from com.DofusClient import DofusClient
from com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager

import com.ankamagames.dofus.kernel.net.ConnectionsHandler as connh
from com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from com.ankamagames.atouin.messages.EntityMovementCompleteMessage import EntityMovementCompleteMessage
from com.ankamagames.atouin.messages.EntityMovementStoppedMessage import EntityMovementStoppedMessage
from com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from com.ankamagames.dofus.kernel.Kernel import Kernel
from com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from com.ankamagames.dofus.logic.game.common.managers.MapMovementAdapter import MapMovementAdapter
from com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from com.ankamagames.dofus.logic.game.fight.messages.FightRequestFailed import FightRequestFailed
from com.ankamagames.dofus.logic.game.fight.messages.MapMoveFailed import MapMoveFailed
from com.ankamagames.dofus.logic.game.roleplay.actions.PlayerFightRequestAction import PlayerFightRequestAction
from com.ankamagames.dofus.logic.game.roleplay.messages.CharacterMovementStoppedMessage import (
    CharacterMovementStoppedMessage,
)
from com.ankamagames.dofus.logic.game.roleplay.messages.FollowActorFailedMessage import FollowActorFailedMessage
from com.ankamagames.dofus.network.enums.PlayerLifeStatusEnum import PlayerLifeStatusEnum
from com.ankamagames.dofus.network.messages.game.context.GameMapMovementCancelMessage import (
    GameMapMovementCancelMessage,
)
from com.ankamagames.dofus.network.messages.game.context.GameMapMovementConfirmMessage import (
    GameMapMovementConfirmMessage,
)
from com.ankamagames.dofus.network.messages.game.context.GameMapMovementMessage import GameMapMovementMessage
from com.ankamagames.dofus.network.messages.game.context.GameMapMovementRequestMessage import (
    GameMapMovementRequestMessage,
)
from com.ankamagames.dofus.network.messages.game.context.GameMapNoMovementMessage import GameMapNoMovementMessage
from com.ankamagames.dofus.network.messages.game.context.fight.GameFightJoinRequestMessage import (
    GameFightJoinRequestMessage,
)
from com.ankamagames.dofus.network.messages.game.context.roleplay.ChangeMapMessage import ChangeMapMessage
from com.ankamagames.dofus.network.messages.game.context.roleplay.delay.GameRolePlayDelayedActionFinishedMessage import (
    GameRolePlayDelayedActionFinishedMessage,
)
from com.ankamagames.dofus.network.messages.game.context.roleplay.fight.GameRolePlayAttackMonsterRequestMessage import (
    GameRolePlayAttackMonsterRequestMessage,
)
from com.ankamagames.dofus.network.messages.game.context.roleplay.fight.GameRolePlayFightRequestCanceledMessage import (
    GameRolePlayFightRequestCanceledMessage,
)
from com.ankamagames.dofus.network.messages.game.context.roleplay.havenbag.EditHavenBagFinishedMessage import (
    EditHavenBagFinishedMessage,
)
from com.ankamagames.dofus.network.messages.game.context.roleplay.MapChangeFailedMessage import MapChangeFailedMessage
from com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataMessage import (
    MapComplementaryInformationsDataMessage,
)
from com.ankamagames.dofus.network.messages.game.context.roleplay.TeleportOnSameMapMessage import (
    TeleportOnSameMapMessage,
)
from com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogMessage import LeaveDialogMessage
from com.ankamagames.dofus.network.messages.game.guild.tax.GuildFightPlayersHelpersLeaveMessage import (
    GuildFightPlayersHelpersLeaveMessage,
)
from com.ankamagames.dofus.network.messages.game.interactive.InteractiveUsedMessage import InteractiveUsedMessage
from com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseEndedMessage import (
    InteractiveUseEndedMessage,
)
from com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseErrorMessage import (
    InteractiveUseErrorMessage,
)
from com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseRequestMessage import (
    InteractiveUseRequestMessage,
)
from com.ankamagames.dofus.network.messages.game.interactive.skill.InteractiveUseWithParamRequestMessage import (
    InteractiveUseWithParamRequestMessage,
)
from com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeLeaveMessage import ExchangeLeaveMessage
from com.ankamagames.dofus.network.messages.game.prism.PrismFightDefenderLeaveMessage import (
    PrismFightDefenderLeaveMessage,
)
from com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import GameContextActorInformations
from com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayGroupMonsterInformations import (
    GameRolePlayGroupMonsterInformations,
)
from com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import InteractiveElement
from com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from com.ankamagames.jerakine.entities.interfaces.IMovable import IMovable
from com.ankamagames.jerakine.handlers.messages.Action import Action
from com.ankamagames.jerakine.logger.Logger import Logger
from com.ankamagames.jerakine.messages.Frame import Frame
from com.ankamagames.jerakine.messages.Message import Message
from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.jerakine.pathfinding.Pathfinding import Pathfinding
from com.ankamagames.jerakine.types.enums.Priority import Priority
from com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from com.ankamagames.jerakine.types.positions.MovementPath import MovementPath

if TYPE_CHECKING:
    from com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayEntitiesFrame import RoleplayEntitiesFrame
    from com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayInteractivesFrame import RoleplayInteractivesFrame


logger = Logger("Dofus2")


class RoleplayMovementFrame(Frame):
    CONSECUTIVE_MOVEMENT_DELAY: int = 0.25
    VERBOSE = True
    CHANGEMAP_TIMEOUT = 3
    ATTACKMOSTERS_TIMEOUT = 3
    JOINFIGHT_TIMEOUT = 3
    _wantToChangeMap: float = None

    _changeMapByAutoTrip: bool = False

    _followingMove: MapPoint

    _followingIe: object

    _followingMonsterGroup: GameRolePlayGroupMonsterInformations

    _followingMessage = None

    _isRequestingMovement: bool

    _latestMovementRequest: int

    _destinationPoint: int

    _lastPlayerValidatedPosition: MapPoint

    _lastMoveEndCellId: int

    _canMove: bool = True

    _mapHasAggressiveMonsters: bool = False

    _isMoving = False

    _followingActorId = None

    _movementAnimTimer = None

    def __init__(self):
        self._wantToChangeMap = None
        self._changeMapByAutoTrip = False
        self._followingIe = None
        self._followingMonsterGroup = None
        self._followingMove = None
        self._isRequestingMovement = False
        self._latestMovementRequest = 0
        self._lastMoveEndCellId = None
        self._changeMapTimeout = None
        self._changeMapFails = 0
        self._requestFightTimeout = None
        self._requestFighFails = 0
        self._moveRequetFails = 0
        self._isMoving = False
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def isRequestingMovement(self) -> bool:
        return self._isRequestingMovement

    @property
    def entitiesFrame(self) -> "RoleplayEntitiesFrame":
        return Kernel().getWorker().getFrame("RoleplayEntitiesFrame")

    @property
    def interactivesFrame(self) -> "RoleplayInteractivesFrame":
        return Kernel().getWorker().getFrame("RoleplayInteractivesFrame")

    def pushed(self) -> bool:
        self._wantToChangeMap = None
        self._changeMapByAutoTrip = False
        self._followingIe = None
        self._followingMonsterGroup = None
        self._followingMove = None
        self._isRequestingMovement = False
        self._latestMovementRequest = 0
        self._lastMoveEndCellId = None
        self._changeMapTimeout = None
        self._changeMapFails = 0
        self._requestFightTimeout = None
        self._requestFighFails = 0
        self._moveRequetFails = 0
        self._isMoving = False
        self._movementAnimTimer = None
        self._destinationPoint = None
        self._wantsToJoinFight = None
        self._joinFightTimer: Timer = None
        self._joinFightFails = 0
        return True

    def joinFight(self, fighterId: int, fightId: int) -> None:
        if self._joinFightFails > 3:
            DofusClient().restart()
            return
        gfjrmsg = GameFightJoinRequestMessage()
        gfjrmsg.init(fighterId, fightId)
        ConnectionsHandler.getConnection().send(gfjrmsg)
        if self._joinFightTimer is not None:
            self._joinFightTimer.cancel()
        self._joinFightTimer = Timer(self.JOINFIGHT_TIMEOUT, self.joinFight, [fighterId, fightId])
        self._joinFightTimer.start()
        self._joinFightFails += 1
        logger.debug("Join fight timer started")

    def process(self, msg: Message) -> bool:
        if Kernel().getWorker().contains("FightContextFrame"):
            logger.error("[RolePlayMovement] Trying to perform roleplay action while the player is fighting")
            connh.ConnectionsHandler.getConnection().close()

        if isinstance(msg, GameMapNoMovementMessage):
            logger.debug("[RolePlayMovement] Server rejected Movement!")
            if self._moveRequetFails > 0:
                Kernel().getWorker().process(MapMoveFailed())
                return
            self._moveRequetFails += 1
            if self._changeMapTimeout:
                self._changeMapTimeout.cancel()
            if self._movementAnimTimer:
                self._movementAnimTimer.cancel()
            self._isMoving = False
            self._canMove = True
            self._isRequestingMovement = False
            gmnmm = msg
            newPos = MapPoint.fromCoords(gmnmm.cellX, gmnmm.cellY)
            player: AnimatedCharacter = DofusEntities.getEntity(PlayedCharacterManager().id)
            if not player:
                logger.warn("[RolePlayMovement] Player not found!!")
                return True
            if player.isMoving:
                player.stop = True
            player.position = newPos

            if self._wantsToJoinFight:
                self.joinFight(self._wantsToJoinFight["fighterId"], self._wantsToJoinFight["fightId"])

            elif self._followingIe:
                self.activateSkill(
                    self._followingIe["skillInstanceId"],
                    self._followingIe["ie"].elementId,
                    self._followingIe["additionalParam"],
                )
                self._followingIe = None

            elif self._followingMonsterGroup:
                self.requestMonsterFight(self._followingMonsterGroup.contextualId)
                self._followingMonsterGroup = None

            elif self._wantToChangeMap is not None:
                if self._destinationPoint is not None:
                    mp = MapPoint.fromCellId(self._destinationPoint)
                    if newPos == mp:
                        self.askMapChange()
                    else:
                        self.askMoveTo(mp)
                else:
                    self.askMapChange()

            elif self._followingActorId:
                self.setFollowingActor(self._followingActorId)

            return True

        if isinstance(msg, GameMapMovementMessage):
            gmmmsg = msg
            movedEntity = DofusEntities.getEntity(gmmmsg.actorId)
            clientMovePath = MapMovementAdapter.getClientMovement(gmmmsg.keyMovements)
            if movedEntity:
                if self.VERBOSE:
                    logger.info(
                        f"[MapMovement] Entity {movedEntity.id} moved from {movedEntity.position.cellId} to {clientMovePath.end.cellId}"
                    )
                movedEntity.position.cellId = clientMovePath.end.cellId
                self.entitiesFrame.updateEntityCellId(gmmmsg.actorId, clientMovePath.end.cellId)
            else:
                logger.warning(f"[MapMovement] Entity {gmmmsg.actorId} not found")

            if float(gmmmsg.actorId) != float(PlayedCharacterManager().id):
                self.applyGameMapMovement(float(gmmmsg.actorId), clientMovePath, msg)
                if self._followingActorId and int(msg.actorId) == int(self._followingActorId):
                    logger.debug(f"Followed actor moved to {clientMovePath.end.cellId}")
                    if self._destinationPoint != clientMovePath.end.cellId:
                        if self._isMoving:
                            self.cancelFollowingActor()
                        self._isRequestingMovement = False
                        self.askMoveTo(clientMovePath.end)

            else:
                self._isRequestingMovement = False
                self._isMoving = True
                if (PlayedCharacterManager().inventoryWeight / PlayedCharacterManager().inventoryWeightMax) == 1:
                    pathDuration = max(1, 1 * clientMovePath.getCrossingDuration(False))
                else:
                    pathDuration = max(1, 1 * clientMovePath.getCrossingDuration(True))
                if self._movementAnimTimer:
                    self._movementAnimTimer.cancel()
                self._movementAnimTimer = Timer(pathDuration * 1.3, self.onMovementAnimEnd, [movedEntity])
                self._isMoving = True
                self._destinationPoint = clientMovePath.end.cellId
                self._movementAnimTimer.start()
                logger.debug(f"Movement anim timer started")
            return True

        elif isinstance(msg, EntityMovementCompleteMessage):
            emcmsg = msg
            if self._movementAnimTimer:
                self._movementAnimTimer.cancel()
            if emcmsg.entity.id == PlayedCharacterManager().id:

                if self.VERBOSE:
                    logger.debug(
                        f"[RolePlayMovement] Mouvement complete, arrived at {emcmsg.entity.position.cellId} and the requested destination was {self._destinationPoint}"
                    )
                gmmcmsg = GameMapMovementConfirmMessage()
                ConnectionsHandler.getConnection().send(gmmcmsg)

                if self._wantToChangeMap is not None:
                    logger.debug(f"[RolePlayMovement] Wants to change map to {self._wantToChangeMap}")
                    self._isRequestingMovement = False
                    if emcmsg.entity.position.cellId != self._destinationPoint:
                        if self.VERBOSE:
                            logger.debug(
                                f"[RolePlayMovement] Wants to change map but didn't reach the map change cell will retry to reach it"
                            )
                        self.askMoveTo(MapPoint.fromCellId(self._destinationPoint))
                    else:
                        self.askMapChange()

                elif self._followingIe:
                    if self.VERBOSE:
                        logger.debug(
                            f"[RolePlayMovement] Wants to activate element {self._followingIe['ie'].elementId}"
                        )
                    self._isRequestingMovement = False
                    self.activateSkill(
                        self._followingIe["skillInstanceId"],
                        self._followingIe["ie"].elementId,
                        self._followingIe["additionalParam"],
                    )
                    self._followingIe = None

                elif self._followingMonsterGroup:
                    if self.VERBOSE:
                        logger.debug(
                            f"[RolePlayMovement] Wants to attack monster group {self._followingMonsterGroup.contextualId}"
                        )
                    self._isRequestingMovement = False
                    self._followingMonsterGroup = self.entitiesFrame.getEntityInfos(
                        self._followingMonsterGroup.contextualId
                    )
                    freshMonstersPosition = self._followingMonsterGroup.disposition
                    if freshMonstersPosition.cellId == emcmsg.entity.position.cellId:
                        self.requestMonsterFight(self._followingMonsterGroup.contextualId)
                    else:
                        if self.VERBOSE:
                            logger.debug(
                                f"[RolePlayMovement] Monster group {self._followingMonsterGroup.contextualId} changed the position from {emcmsg.entity.position.cellId} to {freshMonstersPosition.cellId}"
                            )
                        self.askMoveTo(MapPoint.fromCellId(freshMonstersPosition.cellId))

                elif self._wantsToJoinFight:
                    self.joinFight(self._wantsToJoinFight["fighterId"], self._wantsToJoinFight["fightId"])

                Kernel().getWorker().processImmediately(CharacterMovementStoppedMessage())
            return True

        elif isinstance(msg, EntityMovementStoppedMessage):
            emsmsg = msg
            if emsmsg.entity.id == PlayedCharacterManager().id:
                canceledMoveMessage = GameMapMovementCancelMessage()
                canceledMoveMessage.init(emsmsg.entity.position.cellId)
                ConnectionsHandler.getConnection().send(canceledMoveMessage)
                self._isRequestingMovement = False
                if self._followingMove and self._canMove:
                    self.askMoveTo(self._followingMove)
                    self._followingMove = None
                if self._followingMessage:
                    if isinstance(self._followingMessage, PlayerFightRequestAction):
                        Kernel().getWorker().process(self._followingMessage)
                    else:
                        ConnectionsHandler.getConnection().send(self._followingMessage)
                    self._followingMessage = None
            return True

        elif isinstance(msg, TeleportOnSameMapMessage):
            tosmmsg = msg
            teleportedEntity = DofusEntities.getEntity(tosmmsg.targetId)
            if teleportedEntity:
                if isinstance(teleportedEntity, IMovable):
                    if teleportedEntity.isMoving:
                        teleportedEntity.stop(True)
                    teleportedEntity
                else:
                    logger.warn("Cannot teleport a non IMovable entity. WTF ?")
            else:
                logger.warn("Received a teleportation request for a non-existing entity. Aborting.")
            return True

        elif isinstance(msg, InteractiveUsedMessage):
            if msg.entityId == PlayedCharacterManager().id:
                self._canMove = msg.canMove
            return False

        elif isinstance(msg, InteractiveUseEndedMessage):
            self._canMove = True
            return False

        elif isinstance(msg, InteractiveUseErrorMessage):
            self._canMove = True
            return False

        elif isinstance(msg, LeaveDialogMessage):
            self._canMove = True
            return False

        elif isinstance(msg, ExchangeLeaveMessage):
            self._canMove = True
            return False

        elif isinstance(msg, EditHavenBagFinishedMessage):
            self._canMove = True
            return False

        elif isinstance(msg, GameRolePlayDelayedActionFinishedMessage):
            if msg.delayedCharacterId == PlayedCharacterManager().id:
                self._canMove = True
            return False

        elif isinstance(msg, GuildFightPlayersHelpersLeaveMessage):
            if msg.playerId == PlayedCharacterManager().id:
                self._canMove = True
            return False

        elif isinstance(msg, PrismFightDefenderLeaveMessage):
            if msg.fighterToRemoveId == PlayedCharacterManager().id:
                self._canMove = True
            return False

        elif isinstance(msg, GameRolePlayFightRequestCanceledMessage):
            if msg.targetId == PlayedCharacterManager().id or msg.sourceId == PlayedCharacterManager().id:
                self._canMove = True
            return False

        elif isinstance(msg, MapComplementaryInformationsDataMessage):
            self._mapHasAggressiveMonsters = msg.hasAggressiveMonsters
            self._isRequestingMovement = False
            return False

        else:
            return False

    def pulled(self) -> bool:
        # logger.debug("[RolePlayMovement] Pulled")
        self._canMove = True
        self._followingMonsterGroup = None
        self._followingIe = None
        self._isRequestingMovement = False
        self._wantToChangeMap = None
        if self._requestFightTimeout:
            self._requestFightTimeout.cancel()
        self._requestFighFails = 0
        if self._changeMapTimeout:
            self._changeMapTimeout.cancel()
        if self._movementAnimTimer:
            self._movementAnimTimer.cancel()
        if self._joinFightTimer:
            self._joinFightTimer.cancel()
        self._destinationPoint = None
        self._followingMove = None
        self._joinFightTimer = None
        return True

    def onMovementAnimEnd(self, movedEntity: IEntity) -> None:
        self._isMoving = False
        KernelEventsManager().dispatch(KernelEventsManager.MOVEMENT_STOPPED)
        Kernel().getWorker().processImmediately(EntityMovementCompleteMessage(movedEntity))

    def setNextMoveMapChange(self, mapId: float, autoTrip: bool = False) -> None:
        self._wantToChangeMap = mapId
        self._changeMapByAutoTrip = autoTrip

    def resetNextMoveMapChange(self) -> None:
        self._wantToChangeMap = None
        if self._changeMapTimeout:
            self._changeMapTimeout.cancel()
        self._changeMapByAutoTrip = False

    def setFollowingInteraction(self, interaction: object) -> None:
        self._followingIe = interaction

    def setFollowingMonsterFight(self, monsterGroup: object) -> None:
        self._followingMonsterGroup = monsterGroup

    def setFollowingMessage(self, message) -> None:
        if not isinstance(message, (INetworkMessage, Action)):
            raise Exception("The message is neither INetworkMessage or Action")
        self._followingMessage = message

    def askMoveTo(self, cell: MapPoint) -> bool:
        playerEntity: AnimatedCharacter = DofusEntities.getEntity(PlayedCharacterManager().id)
        if playerEntity.position.cellId == cell.cellId:
            logger.debug("[RolePlayMovement] Already on the cell")
        logger.debug(
            f"[RolePlayMovement] Asking move from cell {playerEntity.position.cellId} to cell {cell}, can Move {self._canMove}"
        )
        if not self._canMove or PlayedCharacterManager().state == PlayerLifeStatusEnum.STATUS_TOMBSTONE:
            logger.debug("[RolePlayMovement] Can't move or dead, aborting")
            return False
        if self._isRequestingMovement == True:
            logger.error("[RolePlayMovement] Already requesting movement, aborting")
            return False
        now: int = perf_counter()
        nexPossibleMovementTime = self._latestMovementRequest + self.CONSECUTIVE_MOVEMENT_DELAY
        if now < nexPossibleMovementTime:
            sleep(self.CONSECUTIVE_MOVEMENT_DELAY)
        self._isRequestingMovement = True
        if playerEntity is None:
            logger.warn(
                "[RolePlayMovement] The player tried to move before its character was added to the scene. Aborting."
            )
            self._isRequestingMovement = False
            return False
        self._destinationPoint = cell.cellId
        if playerEntity.isMoving:
            self._followingMove = cell
            logger.debug("[RolePlayMovement] Player is already moving, waiting for him to stop")
            return False
        movePath = Pathfinding.findPath(DataMapProvider(), playerEntity.position, cell)
        self.sendPath(movePath)
        return True

    def sendPath(self, path: MovementPath) -> None:
        if path.start.cellId == path.end.cellId:
            if self.VERBOSE:
                logger.warn(
                    f"[RolePlayMovement] Discarding a movement path that begins and ends on the same cell ({path.start.cellId})."
                )
            self._isRequestingMovement = False
            if self._followingIe:
                self.activateSkill(
                    self._followingIe["skillInstanceId"],
                    self._followingIe["ie"].elementId,
                    self._followingIe["additionalParam"],
                )
                self._followingIe = None
            elif self._followingMonsterGroup:
                self._followingMonsterGroup = self.entitiesFrame.getEntityInfos(
                    self._followingMonsterGroup.contextualId
                )
                if self._followingMonsterGroup.disposition.cellId == path.end.cellId:
                    self.requestMonsterFight(self._followingMonsterGroup.contextualId)
                else:
                    self.askMoveTo(MapPoint.fromCellId(self._followingMonsterGroup.disposition.cellId))
            return
        gmmrmsg = GameMapMovementRequestMessage()
        keymoves = MapMovementAdapter.getServerMovement(path)
        gmmrmsg.init(keymoves, MapDisplayManager().currentMapPoint.mapId)
        if self.VERBOSE:
            logger.debug(f"[RolePlayMovement] Sending movement request with keymoves {keymoves}")
        ConnectionsHandler.getConnection().send(gmmrmsg)
        if self.VERBOSE:
            logger.debug(f"[RolePlayMovement] Movement request sent to server.")
        self._latestMovementRequest = perf_counter()

    def applyGameMapMovement(self, actorId: float, movement: MovementPath, forceWalking: bool = False) -> None:
        movedEntity: IEntity = DofusEntities.getEntity(actorId)
        if movedEntity is None:
            logger.warn(
                f"[RolePlayMovement] The entity {actorId} moved before it was added to the scene. Aborting movement."
            )
            return
        self._lastMoveEndCellId = movement.end.cellId
        if movedEntity.id == PlayedCharacterManager().id:
            self._isRequestingMovement = False

    def askMapChange(self) -> None:
        if self._wantToChangeMap is None:
            logger.debug("[RolePlayMovement] Can't request map change to void")
            return
        logger.debug("[RolePlayMovement] Asking for a map change to map " + str(self._wantToChangeMap))
        cmmsg: ChangeMapMessage = ChangeMapMessage()
        cmmsg.init(int(self._wantToChangeMap), False)
        ConnectionsHandler.getConnection().send(cmmsg)
        if self._changeMapTimeout:
            self._changeMapTimeout.cancel()
        self._changeMapTimeout = BenchmarkTimer(self.CHANGEMAP_TIMEOUT, self.onMapChangeFailed)
        self._changeMapTimeout.start()
        if self.VERBOSE:
            logger.debug("[RolePlayMovement] Change map timer started.")

    def attackMonsters(self, contextualId: int) -> None:
        if self._followingMonsterGroup:
            logger.warn("[RolePlayMovement] Already following a monster group, aborting")
            return
        entityInfo = self.entitiesFrame.getEntityInfos(contextualId)
        logger.debug("[RolePlayMovement] Asking for a fight against monsters " + str(entityInfo.contextualId))
        if PlayedCharacterManager().currentCellId == entityInfo.disposition.cellId:
            self.requestMonsterFight(contextualId)
        else:
            self.setFollowingMonsterFight(entityInfo)
            self.askMoveTo(MapPoint.fromCellId(entityInfo.disposition.cellId))

    def setFollowingActor(self, actorId: int) -> None:
        self._followingActorId = actorId
        entityInfo = self.entitiesFrame.getEntityInfos(actorId)
        logger.debug(f"[RolePlayMovement] Asking to follow the actor {actorId}")
        if entityInfo:
            if PlayedCharacterManager().currentCellId != entityInfo.disposition.cellId:
                self.askMoveTo(MapPoint.fromCellId(entityInfo.disposition.cellId))
        else:
            logger.error(f"Actor {actorId} is not on current map.")

    def onMapChangeFailed(self) -> None:
        logger.debug(f"[RolePlayMovement] Map change to {self._wantToChangeMap} failed!")
        if self._changeMapTimeout:
            self._changeMapTimeout.cancel()
        self._changeMapFails += 1
        if self._changeMapFails > 1:
            logger.debug(f"[RolePlayMovement] Change map to dest {self._wantToChangeMap} failed!")
            cmfm: MapChangeFailedMessage = MapChangeFailedMessage()
            cmfm.init(self._wantToChangeMap)
            Kernel().getWorker().processImmediately(cmfm)
        elif self._wantToChangeMap is None:
            logger.error(f"We want to change map to None, aborting")
        else:
            self.askMapChange()
            self._changeMapTimeout = BenchmarkTimer(self.CHANGEMAP_TIMEOUT, self.onMapChangeFailed)
            self._changeMapTimeout.start()

    def activateSkill(self, skillInstanceId: int, elementId: int, additionalParam: int = 0) -> None:
        rpInteractivesFrame: "RoleplayInteractivesFrame" = Kernel().getWorker().getFrame("RoleplayInteractivesFrame")
        if self.VERBOSE:
            logger.debug(
                f"[RolePlayMovement] requested registred Elm: {rpInteractivesFrame.currentRequestedElementId}, wants to activate {elementId} and already using something {rpInteractivesFrame.usingInteractive}"
            )
        if (
            rpInteractivesFrame
            and rpInteractivesFrame.currentRequestedElementId != elementId
            and not rpInteractivesFrame.usingInteractive
        ):
            rpInteractivesFrame.currentRequestedElementId = elementId
            if additionalParam == 0:
                iurmsg = InteractiveUseRequestMessage()
                iurmsg.init(int(elementId), int(skillInstanceId))
                ConnectionsHandler.getConnection().send(iurmsg)
            else:
                iuwprmsg = InteractiveUseWithParamRequestMessage()
                iuwprmsg.init(elementId, skillInstanceId, additionalParam)
                ConnectionsHandler.getConnection().send(iuwprmsg)
            self._canMove = False

    def requestMonsterFight(self, monsterGroupId: int) -> None:
        if self._requestFighFails > 0:
            logger.error(
                f"[RolePlayMovement]  Server rejected moster fight request for the {self._requestFighFails} time!"
            )
            self._requestFighFails = 0
            nopmsg = FightRequestFailed(monsterGroupId)
            Kernel().getWorker().processImmediately(nopmsg)
            return False
        self._followingMonsterGroup = None
        grpamrmsg: GameRolePlayAttackMonsterRequestMessage = GameRolePlayAttackMonsterRequestMessage()
        grpamrmsg.init(monsterGroupId)
        ConnectionsHandler.getConnection().send(grpamrmsg)
        self._requestFightTimeout = BenchmarkTimer(1, lambda: self.attackMonsters(monsterGroupId))
        self._requestFightTimeout.start()
        self._requestFighFails += 1

    def cancelFollowingIe(self):
        if self._movementAnimTimer:
            self._movementAnimTimer.cancel()
        self._isRequestingMovement = False
        self._followingIe = None
        self._canMove = True
        self._isMoving = False
        cmmsg = GameMapMovementCancelMessage()
        cmmsg.init(self._destinationPoint)
        Kernel().getWorker().processImmediately(cmmsg)
        ConnectionsHandler.getConnection().send(cmmsg)

    def cancelFollowingActor(self):
        self._isRequestingMovement = False
        if self._movementAnimTimer:
            self._movementAnimTimer.cancel()
        self._canMove = True
        self._isMoving = False
        cmmsg = GameMapMovementCancelMessage()
        cmmsg.init(self._destinationPoint)
        Kernel().getWorker().processImmediately(cmmsg)
        ConnectionsHandler.getConnection().send(cmmsg)
