from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildJoinedMessage import \
    GuildJoinedMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
        GuildInformations
    

class GuildMembershipMessage(GuildJoinedMessage):
    def init(self, guildInfo_: 'GuildInformations', rankId_: int):
        
        super().init(guildInfo_, rankId_)
    