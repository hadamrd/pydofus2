from com.ankamagames.dofus.kernel.Kernel import Kernel
from com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from com.ankamagames.dofus.network.enums.GameContextEnum import GameContextEnum
from com.ankamagames.dofus.network.messages.game.basic.SequenceNumberMessage import (
    SequenceNumberMessage,
)
from com.ankamagames.dofus.network.messages.game.context.GameContextCreateMessage import GameContextCreateMessage
from com.ankamagames.dofus.network.messages.game.context.roleplay.CurrentMapMessage import CurrentMapMessage
from com.ankamagames.jerakine.logger.Logger import Logger
from com.ankamagames.jerakine.messages.Frame import Frame
from com.ankamagames.jerakine.messages.Message import Message
from com.ankamagames.jerakine.types.enums.Priority import Priority
from com.ankamagames.dofus.network.messages.game.basic.SequenceNumberRequestMessage import (
    SequenceNumberRequestMessage,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayMovementFrame import RoleplayMovementFrame

logger = Logger("pyd2bot")


class SynchronisationFrame(Frame):

    STEP_TIME: int = 2

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.HIGHEST

    def pushed(self) -> bool:
        self._synchroStepByServer = dict()
        return True

    def resetSynchroStepByServer(self, connexionId: str) -> None:
        self._synchroStepByServer[connexionId] = 0

    def process(self, msg: Message) -> bool:
        snrMsg: SequenceNumberRequestMessage = None
        snMsg: SequenceNumberMessage = None

        if isinstance(msg, SequenceNumberRequestMessage):
            snrMsg = msg
            if not self._synchroStepByServer.get(snrMsg.sourceConnection):
                self._synchroStepByServer[snrMsg.sourceConnection] = 0
            self._synchroStepByServer[snrMsg.sourceConnection] += 1
            snMsg = SequenceNumberMessage()
            snMsg.init(number_=self._synchroStepByServer[snrMsg.sourceConnection])
            ConnectionsHandler.getConnection().send(snMsg, snrMsg.sourceConnection)
            return True

        if isinstance(msg, CurrentMapMessage):
            rplmvf: "RoleplayMovementFrame" = Kernel().getWorker().getFrame("RoleplayMovementFrame")
            if rplmvf and rplmvf._changeMapTimeout:
                logger.debug("Cancel change map timeout")
                rplmvf._changeMapTimeout.cancel()
                rplmvf._wantToChangeMap = None
                rplmvf._changeMapFails = 0
            return False

        if isinstance(msg, GameContextCreateMessage):
            if msg.context == GameContextEnum.FIGHT:
                rplmvf: "RoleplayMovementFrame" = Kernel().getWorker().getFrame("RoleplayMovementFrame")
                if rplmvf and rplmvf._requestFightTimeout:
                    rplmvf._requestFightTimeout.cancel()
                    rplmvf._requestFighFails = 0
                    rplmvf._followingMonsterGroup = None
            return False

        else:
            return False

    def pulled(self) -> bool:
        return True
