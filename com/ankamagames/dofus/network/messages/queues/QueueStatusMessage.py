from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage


class QueueStatusMessage(INetworkMessage):
    protocolId = 2197
    position:int
    total:int
    
    
