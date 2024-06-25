from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.network.messages.game.basic.SequenceNumberMessage import SequenceNumberMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.basic.SequenceNumberRequestMessage import (
    SequenceNumberRequestMessage,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority

if TYPE_CHECKING:
    pass


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

        if isinstance(msg, SequenceNumberRequestMessage):
            Logger().debug(f"Server asked for seq for connection {msg.sourceConnection}")
            if msg.sourceConnection not in self._synchroStepByServer:
                self._synchroStepByServer[msg.sourceConnection] = 0
            self._synchroStepByServer[msg.sourceConnection] += 1
            snMsg = SequenceNumberMessage()
            snMsg.init(number_=self._synchroStepByServer[msg.sourceConnection])
            ConnectionsHandler().send(snMsg)
            return True

    def pulled(self) -> bool:
        return True
