from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.paddock.PaddockBuyableInformations import \
    PaddockBuyableInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
        GuildInformations
    

class PaddockGuildedInformations(PaddockBuyableInformations):
    deserted: bool
    guildInfo: 'GuildInformations'
    def init(self, deserted_: bool, guildInfo_: 'GuildInformations', price_: int, locked_: bool):
        self.deserted = deserted_
        self.guildInfo = guildInfo_
        
        super().init(price_, locked_)
    