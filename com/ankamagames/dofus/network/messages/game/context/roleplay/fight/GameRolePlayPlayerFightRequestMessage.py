from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage


class GameRolePlayPlayerFightRequestMessage(INetworkMessage):
    protocolId = 6364
    targetId:int
    targetCellId:int
    friendly:bool
    
    
