from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class AllianceCreationResultMessage(NetworkMessage):
    result:int
    

    def init(self, result:int):
        self.result = result
        
        super().__init__()
    
    