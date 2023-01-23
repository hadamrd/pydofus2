from pydofus2.com.ankamagames.dofus.network.messages.queues.LoginQueueStatusMessage import (
    LoginQueueStatusMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.queues.QueueStatusMessage import (
    QueueStatusMessage,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
logger = Logger("Dofus2")

class QueueFrame(Frame):
    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, LoginQueueStatusMessage):
            logger.debug(f"LoginQueueStatusMessage: position={msg.position}, total={msg.total}")
            return True

        elif isinstance(msg, QueueStatusMessage):
            logger.debug(f"QueueStatusMessage: position={msg.position}, total={msg.total}")
            return True

        else:
            return False

    def pulled(self) -> bool:
        return True
