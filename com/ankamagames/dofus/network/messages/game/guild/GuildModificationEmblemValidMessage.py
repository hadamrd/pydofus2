from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.dofus.network.types.game.guild.GuildEmblem import GuildEmblem


class GuildModificationEmblemValidMessage(INetworkMessage):
    protocolId = 3249
    guildEmblem:GuildEmblem
    
    
