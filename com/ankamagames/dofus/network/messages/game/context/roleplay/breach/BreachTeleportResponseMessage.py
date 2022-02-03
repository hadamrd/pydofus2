from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class BreachTeleportResponseMessage(NetworkMessage):
    teleported:bool
    

    def init(self, teleported:bool):
        self.teleported = teleported
        
        super().__init__()
    
    