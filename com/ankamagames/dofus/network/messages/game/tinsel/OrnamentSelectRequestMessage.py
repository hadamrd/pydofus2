from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class OrnamentSelectRequestMessage(NetworkMessage):
    ornamentId:int
    

    def init(self, ornamentId:int):
        self.ornamentId = ornamentId
        
        super().__init__()
    
    