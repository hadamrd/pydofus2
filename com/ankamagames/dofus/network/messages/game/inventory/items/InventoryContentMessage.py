from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.dofus.network.types.game.data.items.ObjectItem import ObjectItem


class InventoryContentMessage(INetworkMessage):
    protocolId = 4197
    objects:ObjectItem
    kamas:int
    
    
