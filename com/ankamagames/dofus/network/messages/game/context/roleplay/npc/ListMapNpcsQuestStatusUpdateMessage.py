from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.dofus.network.types.game.context.roleplay.npc.MapNpcQuestInfo import MapNpcQuestInfo


class ListMapNpcsQuestStatusUpdateMessage(INetworkMessage):
    protocolId = 5996
    mapInfo:MapNpcQuestInfo
    
    
