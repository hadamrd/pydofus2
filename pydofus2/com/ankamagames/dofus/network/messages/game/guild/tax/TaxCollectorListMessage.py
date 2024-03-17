from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.guild.tax.AbstractTaxCollectorListMessage import \
    AbstractTaxCollectorListMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.tax.TaxCollectorFightersInformation import \
        TaxCollectorFightersInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.tax.TaxCollectorInformations import \
        TaxCollectorInformations
    

class TaxCollectorListMessage(AbstractTaxCollectorListMessage):
    nbcollectorMax: int
    fightersInformations: list['TaxCollectorFightersInformation']
    infoType: int
    def init(self, nbcollectorMax_: int, fightersInformations_: list['TaxCollectorFightersInformation'], infoType_: int, informations_: list['TaxCollectorInformations']):
        self.nbcollectorMax = nbcollectorMax_
        self.fightersInformations = fightersInformations_
        self.infoType = infoType_
        
        super().init(informations_)
    