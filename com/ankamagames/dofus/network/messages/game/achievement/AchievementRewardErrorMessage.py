from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class AchievementRewardErrorMessage(NetworkMessage):
    achievementId:int
    

    def init(self, achievementId:int):
        self.achievementId = achievementId
        
        super().__init__()
    
    