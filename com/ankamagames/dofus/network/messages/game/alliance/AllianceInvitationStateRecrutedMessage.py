from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class AllianceInvitationStateRecrutedMessage(NetworkMessage):
    invitationState:int
    

    def init(self, invitationState:int):
        self.invitationState = invitationState
        
        super().__init__()
    
    