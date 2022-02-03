from com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyEventMessage import AbstractPartyEventMessage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyMemberInformations import PartyMemberInformations
    


class PartyUpdateMessage(AbstractPartyEventMessage):
    memberInformations:'PartyMemberInformations'
    

    def init(self, memberInformations:'PartyMemberInformations', partyId:int):
        self.memberInformations = memberInformations
        
        super().__init__(partyId)
    
    