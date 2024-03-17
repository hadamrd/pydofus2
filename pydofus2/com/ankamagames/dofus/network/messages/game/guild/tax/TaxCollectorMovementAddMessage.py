from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.tax.TaxCollectorInformations import \
        TaxCollectorInformations
    

class TaxCollectorMovementAddMessage(NetworkMessage):
    informations: 'TaxCollectorInformations'
    def init(self, informations_: 'TaxCollectorInformations'):
        self.informations = informations_
        
        super().__init__()
    