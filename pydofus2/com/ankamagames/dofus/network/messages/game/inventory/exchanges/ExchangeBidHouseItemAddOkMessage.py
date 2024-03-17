from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSellInBid import \
        ObjectItemToSellInBid
    

class ExchangeBidHouseItemAddOkMessage(NetworkMessage):
    itemInfo: 'ObjectItemToSellInBid'
    def init(self, itemInfo_: 'ObjectItemToSellInBid'):
        self.itemInfo = itemInfo_
        
        super().__init__()
    