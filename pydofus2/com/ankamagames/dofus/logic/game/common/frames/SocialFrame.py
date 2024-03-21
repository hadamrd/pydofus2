from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.people.SocialCharacterWrapper import SocialCharacterWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.GuildDialogFrame import \
    GuildDialogFrame
from pydofus2.com.ankamagames.dofus.network.enums.GuildInformationsTypeEnum import GuildInformationsTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.PlayerStatusEnum import \
    PlayerStatusEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.alliance.AllianceRanksRequestMessage import AllianceRanksRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.alliance.application.AllianceGetPlayerApplicationMessage import AllianceGetPlayerApplicationMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.status.PlayerStatusUpdateMessage import \
    PlayerStatusUpdateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.status.PlayerStatusUpdateRequestMessage import \
    PlayerStatusUpdateRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.friend.AcquaintancesGetListMessage import AcquaintancesGetListMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.friend.FriendsGetListMessage import FriendsGetListMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.friend.IgnoredGetListMessage import IgnoredGetListMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.friend.SpouseGetInformationsMessage import SpouseGetInformationsMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildGetInformationsMessage import GuildGetInformationsMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildInvitedMessage import \
    GuildInvitedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildRanksRequestMessage import GuildRanksRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.guild.application.GuildGetPlayerApplicationMessage import GuildGetPlayerApplicationMessage
from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import \
    PlayerStatus
from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatusExtended import \
    PlayerStatusExtended
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import StoreDataManager
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
        self._enemiesList = list[SocialCharacterWrapper]()
        self._ignoredList = list[SocialCharacterWrapper]()
        self._guildDialogFrame = GuildDialogFrame()
        # self._allianceDialogFrame = AllianceDialogFrame()
        fglmsg = FriendsGetListMessage()
        fglmsg.init()
        ConnectionsHandler().send(fglmsg)
        amsg = AcquaintancesGetListMessage()
        amsg.init()
        ConnectionsHandler().send(amsg)
        iglmsg = IgnoredGetListMessage()
        iglmsg.init()
        ConnectionsHandler().send(iglmsg)
        sgimsg = SpouseGetInformationsMessage()
        sgimsg.init()
        ConnectionsHandler().send(sgimsg)
        ggimsg = GuildGetInformationsMessage()
        ggimsg.init(GuildInformationsTypeEnum.INFO_MEMBERS)
        ConnectionsHandler().send(ggimsg)
        ggpamsg = GuildGetPlayerApplicationMessage()
        ggpamsg.init()
        ConnectionsHandler().send(ggpamsg)
        grrmsg = GuildRanksRequestMessage()
        grrmsg.init()
        ConnectionsHandler().send(grrmsg)
        apamsg = AllianceGetPlayerApplicationMessage()
        apamsg.init()
        ConnectionsHandler().send(apamsg)
        arrmsg = AllianceRanksRequestMessage()
        arrmsg.init()
        ConnectionsHandler().send(arrmsg)
        # self.enableAchievementWarn(StoreDataManager().getSetData(BeriliaConstants.DATASTORE_UI_OPTIONS, DATA_WARN_FRIEND_ACHIEVEMENT, False))
        # self.enableFriendConnectionWarn(StoreDataManager().getSetData(BeriliaConstants.DATASTORE_UI_OPTIONS, DATA_WARN_FRIEND_CONNECTION, False))
        # self.enableLevelupWarn(StoreDataManager().getSetData(BeriliaConstants.DATASTORE_UI_OPTIONS ,DATA_WARN_FRIEND_LEVELUP, False))
        # self.enablePermaDeathWarn(StoreDataManager().getSetData(BeriliaConstants.DATASTORE_UI_OPTIONS, DATA_WARN_FRIEND_PERMA_DEATH, False))
        # self.enableShareStatusToFriends(StoreDataManager().getSetData(BeriliaConstants.DATASTORE_UI_OPTIONS, DATA_FRIEND_SHARE_STATUS, False))
        # self.fillRanksIconsList()
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