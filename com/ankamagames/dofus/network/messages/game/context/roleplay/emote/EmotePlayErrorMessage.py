from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class EmotePlayErrorMessage(NetworkMessage):
    emoteId:int
    

    def init(self, emoteId:int):
        self.emoteId = emoteId
        
        super().__init__()
    
    