from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class AllianceInvitationAnswerMessage(NetworkMessage):
    accept:bool
    

    def init(self, accept:bool):
        self.accept = accept
        
        super().__init__()
    
    