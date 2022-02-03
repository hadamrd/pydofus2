from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSell import ObjectItemToSell
    


class ExchangeShopStockStartedMessage(NetworkMessage):
    objectsInfos:list['ObjectItemToSell']
    

    def init(self, objectsInfos:list['ObjectItemToSell']):
        self.objectsInfos = objectsInfos
        
        super().__init__()
    
    