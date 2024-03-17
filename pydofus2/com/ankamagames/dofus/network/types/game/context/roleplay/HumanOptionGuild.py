from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOption import \
    HumanOption

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
        GuildInformations
    

class HumanOptionGuild(HumanOption):
    guildInformations: 'GuildInformations'
    def init(self, guildInformations_: 'GuildInformations'):
        self.guildInformations = guildInformations_
        
        super().init()
    