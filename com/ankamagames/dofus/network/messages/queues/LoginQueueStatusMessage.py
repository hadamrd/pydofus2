from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class LoginQueueStatusMessage(NetworkMessage):
    position:int
    total:int
    

    def init(self, position:int, total:int):
        self.position = position
        self.total = total
        
        super().__init__()
    
    