from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.dofus.network.types.game.achievement.Achievement import Achievement


class AchievementDetailsMessage(INetworkMessage):
    protocolId = 5303
    achievement:Achievement
    
    
