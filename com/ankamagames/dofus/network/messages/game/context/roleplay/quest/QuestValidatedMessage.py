from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class QuestValidatedMessage(NetworkMessage):
    questId:int
    

    def init(self, questId_:int):
        self.questId = questId_
        
        super().__init__()
    
    