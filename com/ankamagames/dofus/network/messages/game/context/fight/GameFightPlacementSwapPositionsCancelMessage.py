from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GameFightPlacementSwapPositionsCancelMessage(NetworkMessage):
    requestId:int
    

    def init(self, requestId:int):
        self.requestId = requestId
        
        super().__init__()
    
    