from time import perf_counter
from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import (
    KernelEvent, KernelEventsManager)
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.MapMovementAdapter import \
    MapMovementAdapter
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import \
    DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.types.RequestTypeEnum import \
    RequestTypesEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementMessage import \
    GameMapMovementMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapNoMovementMessage import \
    GameMapNoMovementMessage

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.fight.GameRolePlayFightRequestCanceledMessage import \
    GameRolePlayFightRequestCanceledMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.havenbag.EditHavenBagFinishedMessage import \
    EditHavenBagFinishedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogMessage import \
    LeaveDialogMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUsedMessage import \
    InteractiveUsedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseEndedMessage import \
    InteractiveUseEndedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseErrorMessage import \
    InteractiveUseErrorMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeLeaveMessage import \
    ExchangeLeaveMessage
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import \
    BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayEntitiesFrame import \
        RoleplayEntitiesFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayInteractivesFrame import \
        RoleplayInteractivesFrame

class RoleplayMovementFrame(Frame):
    VERBOSE = False
    CHANGEMAP_TIMEOUT = 10
    ATTACKMOSTERS_TIMEOUT = 10
    JOINFIGHT_TIMEOUT = 10
    REQUEST_TIMEOUT = 3
    MAX_MOVEMENT_REQUEST_FAILS = 3

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
    def entitiesFrame(self) -> "RoleplayEntitiesFrame":
        return Kernel().worker.getFrameByName("RoleplayEntitiesFrame")

    @property
    def interactivesFrame(self) -> "RoleplayInteractivesFrame":
        return Kernel().worker.getFrameByName("RoleplayInteractivesFrame")

    def pushed(self) -> bool:
        self.isMoving = False
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameMapNoMovementMessage):
            newPos = MapPoint.fromCoords(msg.cellX, msg.cellY)
            self.isMoving = False
            self.canMove = True
            player = DofusEntities().getEntity(PlayedCharacterManager().id)
            player.position = newPos
            self.entitiesFrame.updateEntityCellId(PlayedCharacterManager().id, newPos.cellId)            
            KernelEventsManager().send(KernelEvent.MOVEMENT_STOPPED, newPos)
            return True

        if isinstance(msg, GameMapMovementMessage):
            movedEntity = DofusEntities().getEntity(msg.actorId)
            clientMovePath = MapMovementAdapter.getClientMovement(msg.keyMovements)
            startCell = clientMovePath.start.cellId
            endCell = clientMovePath.end.cellId
            if movedEntity:
                Logger().info(f"[MapMovement] Entity {msg.actorId} moved from cell {startCell} to cell {endCell}.")
                movedEntity.position.cellId = endCell
                self.entitiesFrame.updateEntityCellId(msg.actorId, endCell)
            else:
                Logger().error(f"[MapMovement] Entity {msg.actorId} not found.")
            KernelEventsManager().send(KernelEvent.ENTITY_MOVED, msg.actorId, clientMovePath)
            return True

        elif isinstance(msg, (InteractiveUseEndedMessage, InteractiveUseErrorMessage, LeaveDialogMessage, ExchangeLeaveMessage, EditHavenBagFinishedMessage)):
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

    def pulled(self) -> bool:
        self.canMove = True
        return True
