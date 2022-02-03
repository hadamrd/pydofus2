from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class QuestStepStartedMessage(NetworkMessage):
    questId:int
    stepId:int
    

    def init(self, questId:int, stepId:int):
        self.questId = questId
        self.stepId = stepId
        
        super().__init__()
    
    