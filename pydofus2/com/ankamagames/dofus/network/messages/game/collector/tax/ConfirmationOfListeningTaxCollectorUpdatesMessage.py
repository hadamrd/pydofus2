from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorInformations import \
        TaxCollectorInformations
    

class ConfirmationOfListeningTaxCollectorUpdatesMessage(NetworkMessage):
    information: 'TaxCollectorInformations'
    def init(self, information_: 'TaxCollectorInformations'):
        self.information = information_
        
        super().__init__()
    