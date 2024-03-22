from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.npc.NpcDialogCreationMessage import \
    NpcDialogCreationMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.npc.NpcDialogQuestionMessage import \
    NpcDialogQuestionMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class NpcFrame(Frame):

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        return True

    def pulled(self):
        return True

    def process(self, msg) -> bool:

        if isinstance(msg, NpcDialogCreationMessage):
            KernelEventsManager().send(KernelEvent.NpcDialogOpen, msg.mapId, msg.npcId)
            return True

        elif isinstance(msg, NpcDialogQuestionMessage):
            KernelEventsManager().send(KernelEvent.NpcQuestion, msg.messageId, msg.dialogParams, msg.visibleReplies)
            return True

