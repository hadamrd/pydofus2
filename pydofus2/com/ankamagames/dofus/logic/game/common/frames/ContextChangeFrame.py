from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.PanicMessages import PanicMessages
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.GameContextQuitAction import (
    GameContextQuitAction,
)
from pydofus2.com.ankamagames.dofus.network.enums.GameContextEnum import GameContextEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextCreateMessage import (
    GameContextCreateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextQuitMessage import (
    GameContextQuitMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.CurrentMapMessage import CurrentMapMessage
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority

logger = Logger("Dofus2")


class ContextChangeFrame(Frame):
    def __init__(self):
        self.mapChangeConnexion = ""
        self.currentContext = None
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.LOW

    def pushed(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameContextCreateMessage):
            self.currentContext = msg.context
            if self.currentContext == GameContextEnum.ROLE_PLAY:
                import pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayContextFrame as rplCF
                Kernel().worker.addFrame(rplCF.RoleplayContextFrame())

            elif self.currentContext == GameContextEnum.FIGHT:
                logger.debug("Fight context started")
                import pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame as fcf
                Kernel().worker.addFrame(fcf.FightContextFrame())

            else:
                Kernel().panic(PanicMessages.WRONG_CONTEXT_CREATED, [self.currentContext])

            return False

        if isinstance(msg, GameContextQuitAction):
            gcqmsg = GameContextQuitMessage()
            ConnectionsHandler()._conn.send(gcqmsg)
            return True

        if isinstance(msg, CurrentMapMessage):
            mcmsg = msg
            self.mapChangeConnexion = mcmsg.sourceConnection
            return False

        else:
            return False

    def pulled(self) -> bool:
        return True
