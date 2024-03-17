from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.guild.tax.AbstractTaxCollectorListMessage import \
    AbstractTaxCollectorListMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.tax.TaxCollectorInformations import \
        TaxCollectorInformations
    

class TopTaxCollectorListMessage(AbstractTaxCollectorListMessage):
    isDungeon: bool
    def init(self, isDungeon_: bool, informations_: list['TaxCollectorInformations']):
        self.isDungeon = isDungeon_
        
        super().init(informations_)
    