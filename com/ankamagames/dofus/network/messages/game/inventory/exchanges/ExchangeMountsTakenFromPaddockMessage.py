from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage


class ExchangeMountsTakenFromPaddockMessage(INetworkMessage):
    protocolId = 2526
    name:str
    worldX:int
    worldY:int
    ownername:str
    
    
