from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSellInBid import ObjectItemToSellInBid


class ExchangeBidHouseItemAddOkMessage(INetworkMessage):
    protocolId = 7844
    itemInfo:ObjectItemToSellInBid
    
    
