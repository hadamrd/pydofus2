from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class PresetUseResultMessage(NetworkMessage):
    presetId:int
    code:int
    

    def init(self, presetId:int, code:int):
        self.presetId = presetId
        self.code = code
        
        super().__init__()
    
    