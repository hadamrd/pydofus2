from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.network.enums.DialogTypeEnum import \
    DialogTypeEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogMessage import \
    LeaveDialogMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildInvitationAnswerMessage import \
    GuildInvitationAnswerMessage
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class GuildDialogFrame:
    guildEmblem = None
    
    def __init__(self) -> None:
        super().__init__()
        self._guildDialogFrame = None

    @property
    def priority(cls):
        return Priority.NORMAL

    def pushed(self):
        return True

    @classmethod
    def process(self, msg: Message) -> bool:
        
        if isinstance(msg, LeaveDialogMessage):
            ldm = msg
            Kernel().worker.addFrame(self._guildDialogFrame)
            if ldm.dialogType in [
                DialogTypeEnum.DIALOG_GUILD_CREATE,
                DialogTypeEnum.DIALOG_GUILD_INVITATION,
                DialogTypeEnum.DIALOG_GUILD_RENAME,
            ]:
                self.leaveDialog()
            return True
        return False

    def guildInvitationAnswer(self, accept: bool):
        giamsg = GuildInvitationAnswerMessage().init(accept)
        ConnectionsHandler().send(giamsg)
        self.leaveDialog()

    def leaveDialog(self):
        Kernel().worker.removeFrame(self)
        
    def pulled(self) -> bool:
        KernelEventsManager().send(KernelEvent.LeaveDialog)
        return True