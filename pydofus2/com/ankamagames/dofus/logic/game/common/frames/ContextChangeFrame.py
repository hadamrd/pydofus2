from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.GameContextQuitAction import GameContextQuitAction
from pydofus2.com.ankamagames.dofus.network.enums.GameContextEnum import GameContextEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextCreateMessage import (
    GameContextCreateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextDestroyMessage import (
    GameContextDestroyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextQuitMessage import GameContextQuitMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


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

        if isinstance(msg, GameContextDestroyMessage):
            return True

        elif isinstance(msg, GameContextCreateMessage):
            self.currentContext = msg.context
            if self.currentContext == GameContextEnum.ROLE_PLAY:
                from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayContextFrame import (
                    RoleplayContextFrame,
                )

                Kernel().worker.addFrame(RoleplayContextFrame())
                KernelEventsManager().send(KernelEvent.RoleplayStarted)

            elif self.currentContext == GameContextEnum.FIGHT:
                from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import FightContextFrame

                if not Kernel().isMule:
                    Kernel().worker.addFrame(FightContextFrame())
                KernelEventsManager().send(KernelEvent.FightStarted)
            return True

        elif isinstance(msg, GameContextQuitAction):
            gcqmsg = GameContextQuitMessage()
            ConnectionsHandler().send(gcqmsg)
            return True

    def pulled(self) -> bool:
        return True
