from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.GuildDialogFrame import \
    GuildDialogFrame
from pydofus2.com.ankamagames.dofus.network.enums.PlayerStatusEnum import \
    PlayerStatusEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.character.status.PlayerStatusUpdateMessage import \
    PlayerStatusUpdateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.status.PlayerStatusUpdateRequestMessage import \
    PlayerStatusUpdateRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildInvitedMessage import \
    GuildInvitedMessage
from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import \
    PlayerStatus
from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatusExtended import \
    PlayerStatusExtended
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class SocialFrame(Frame):


    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        self._guildDialogFrame = GuildDialogFrame()
        return True
    
    def pulled(self) -> bool:
        return True
    
    @classmethod
    def updateStatus(cls, status: PlayerStatusEnum):
        pstatus = PlayerStatus()
        pstatus.init(status)
        psurmsg = PlayerStatusUpdateRequestMessage()
        psurmsg.init(pstatus)
        ConnectionsHandler().send(psurmsg)

    def process(self, msg: Message) -> bool:
        
        if isinstance(msg, GuildInvitedMessage):
            Kernel().worker.addFrame(self._guildDialogFrame)
            KernelEventsManager().send(KernelEvent.GuildInvited, msg.guildInfo, msg.recruterName)
            return True
        
        if isinstance(msg, PlayerStatusUpdateMessage):
            message = ""
            if isinstance(msg.status, PlayerStatusExtended):
                message = msg.status.message
            KernelEventsManager().send(KernelEvent.PlayerStatusUpdate, msg.accountId, msg.playerId, msg.status.statusId, message)
            return True