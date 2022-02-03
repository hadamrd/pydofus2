from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class TreasureHuntFlagRequestMessage(NetworkMessage):
    questType:int
    index:int
    

    def init(self, questType:int, index:int):
        self.questType = questType
        self.index = index
        
        super().__init__()
    
    