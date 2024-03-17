from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicGuildInformations import \
        BasicGuildInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.tax.TaxCollectorBasicInformations import \
        TaxCollectorBasicInformations
    

class TaxCollectorAttackedResultMessage(NetworkMessage):
    deadOrAlive: bool
    basicInfos: 'TaxCollectorBasicInformations'
    guild: 'BasicGuildInformations'
    def init(self, deadOrAlive_: bool, basicInfos_: 'TaxCollectorBasicInformations', guild_: 'BasicGuildInformations'):
        self.deadOrAlive = deadOrAlive_
        self.basicInfos = basicInfos_
        self.guild = guild_
        
        super().__init__()
    