from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ObjectDeleteMessage(NetworkMessage):
    objectUID:int
    quantity:int
    

    def init(self, objectUID:int, quantity:int):
        self.objectUID = objectUID
        self.quantity = quantity
        
        super().__init__()
    
    