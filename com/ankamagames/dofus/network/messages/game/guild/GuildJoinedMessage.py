from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import GuildInformations


class GuildJoinedMessage(INetworkMessage):
    protocolId = 1218
    guildInfo:GuildInformations
    memberRights:int
    
    
