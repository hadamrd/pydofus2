from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemGenericQuantity import \
        ObjectItemGenericQuantity
    

class ExchangeBidHouseUnsoldItemsMessage(NetworkMessage):
    items: list['ObjectItemGenericQuantity']
    def init(self, items_: list['ObjectItemGenericQuantity']):
        self.items = items_
        
        super().__init__()
    