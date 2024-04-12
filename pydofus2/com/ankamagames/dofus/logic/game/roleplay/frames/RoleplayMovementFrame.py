from pydofus2.com.ClientStatusEnum import ClientStatusEnum
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InactivityManager import InactivityManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.MapMovementAdapter import MapMovementAdapter
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.types.RequestTypeEnum import RequestTypesEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementConfirmMessage import (
    GameMapMovementConfirmMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementMessage import GameMapMovementMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementRequestMessage import (
    GameMapMovementRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapNoMovementMessage import (
    GameMapNoMovementMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.fight.GameRolePlayFightRequestCanceledMessage import (
    GameRolePlayFightRequestCanceledMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.havenbag.EditHavenBagFinishedMessage import (
    EditHavenBagFinishedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogMessage import LeaveDialogMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUsedMessage import (
    InteractiveUsedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseEndedMessage import (
    InteractiveUseEndedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseErrorMessage import (
    InteractiveUseErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeLeaveMessage import (
    ExchangeLeaveMessage,
)
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class RoleplayMovementFrame(Frame):
    VERBOSE = False
    CHANGEMAP_TIMEOUT = 10
    ATTACKMOSTERS_TIMEOUT = 10
    JOINFIGHT_TIMEOUT = 10
    REQUEST_TIMEOUT = 3
    MAX_MOVEMENT_REQUEST_FAILS = 3
    LOG_OTHER_ENTITIES_MOVEMENT = False

    def __init__(self):
        self.requestType: RequestTypesEnum = None
        self.requestTimer: BenchmarkTimer = None
        self.isMoving = False
        self.movementAnimTimer = None
        self.latestMovementRequest = None
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def requestingMovement(self) -> bool:
        return self.requestingMovement

    @property
    def entitiesFrame(self):
        return Kernel().roleplayEntitiesFrame

    @property
    def interactivesFrame(self):
        return Kernel().interactivesFrame

    def pushed(self) -> bool:
        self.isMoving = False
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameMapNoMovementMessage):
            newPos = MapPoint.fromCoords(msg.cellX, msg.cellY)
            self.isMoving = False
            self.canMove = True
            player: AnimatedCharacter = DofusEntities().getEntity(PlayedCharacterManager().id)
            if player:
                player.isMoving = False
                player.position = newPos
                self.entitiesFrame.updateEntityCellId(PlayedCharacterManager().id, newPos.cellId)
                Logger().debug(f"Movement reject : {newPos}")
                KernelEventsManager().send(KernelEvent.MovementRequestRejected)
                KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.MOVEMENT_REJECTED)
            else:
                Logger().error(
                    "Movement reject received but player data not loaded yet, maybe map changed after a map move request that was rejected."
                )
            return True

        if isinstance(msg, GameMapMovementMessage):
            movedEntity = DofusEntities().getEntity(msg.actorId)
            clientMovePath = MapMovementAdapter.getClientMovement(msg.keyMovements)
            startCell = clientMovePath.start.cellId
            endCell = clientMovePath.end.cellId
            if msg.actorId == PlayedCharacterManager().id:
                Logger().debug(f"Current Player moving from {startCell} to {endCell}.")
            else:
                if self.LOG_OTHER_ENTITIES_MOVEMENT:
                    Logger().debug(f"Entity '{msg.actorId}' moving from {startCell} to {endCell}.")
            if movedEntity:
                movedEntity.position.cellId = endCell
                self.entitiesFrame.updateEntityCellId(msg.actorId, endCell)
            else:
                Logger().warning(f"Actor '{msg.actorId}' moved before it was added to the scene.")
            if msg.actorId == PlayedCharacterManager().id:
                PlayedCharacterManager().entity.move(clientMovePath, self.onPlayerMovementEnded)
                KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.MOVEMENT_IN_PROGRESS, {"path_cells": [cell.cellId for cell in clientMovePath]})
            KernelEventsManager().send(KernelEvent.EntityMoving, msg.actorId, clientMovePath)
            return True

        elif isinstance(
            msg,
            (
                InteractiveUseEndedMessage,
                InteractiveUseErrorMessage,
                LeaveDialogMessage,
                ExchangeLeaveMessage,
                EditHavenBagFinishedMessage,
            ),
        ):
            self.canMove = True
            return False

        elif isinstance(msg, InteractiveUsedMessage):
            if msg.entityId == PlayedCharacterManager().id:
                self.canMove = msg.canMove
            return False

        elif isinstance(msg, GameRolePlayFightRequestCanceledMessage):
            if msg.targetId == PlayedCharacterManager().id or msg.sourceId == PlayedCharacterManager().id:
                self.canMove = True
            return False

        else:
            return False

    def onPlayerMovementEnded(self, success):
        if success:
            gmmcmsg = GameMapMovementConfirmMessage()
            ConnectionsHandler().send(gmmcmsg)
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.MOVEMENT_COMPLETED)
        else:
            Logger().debug("Player didnt complete movement")
        KernelEventsManager().send(KernelEvent.PlayerMovementCompleted, success)

    def sendMovementRequest(self):
        gmmrmsg = GameMapMovementRequestMessage()
        gmmrmsg.init(self.movePath.keyMoves(), MapDisplayManager().currentMapPoint.mapId)
        ConnectionsHandler().send(gmmrmsg)
        KernelEventsManager().send(
            KernelEvent.ClientStatusUpdate,
            ClientStatusEnum.REQUESTING_MAP_MOVEMENT,
            {
                "startCell": PlayedCharacterManager().currentCellId,
                "endCell": self.dstCell.cellId,
                "path": self.movePath,
                "keyMoves": self.movePath.keyMoves(),
            },
        )
        Logger().info(f"Requested move from {PlayedCharacterManager().currentCellId} to {self.dstCell.cellId}")
        InactivityManager().activity()

    def pulled(self) -> bool:
        self.canMove = True
        return True
