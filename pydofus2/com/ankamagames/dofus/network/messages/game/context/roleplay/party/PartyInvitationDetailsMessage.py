from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import \
    AbstractPartyMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyGuestInformations import \
        PartyGuestInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyInvitationMemberInformations import \
        PartyInvitationMemberInformations
    

class PartyInvitationDetailsMessage(AbstractPartyMessage):
    partyType: int
    partyName: str
    fromId: int
    fromName: str
    leaderId: int
    members: list['PartyInvitationMemberInformations']
    guests: list['PartyGuestInformations']
    def init(self, partyType_: int, partyName_: str, fromId_: int, fromName_: str, leaderId_: int, members_: list['PartyInvitationMemberInformations'], guests_: list['PartyGuestInformations'], partyId_: int):
        self.partyType = partyType_
        self.partyName = partyName_
        self.fromId = fromId_
        self.fromName = fromName_
        self.leaderId = leaderId_
        self.members = members_
        self.guests = guests_
        
        super().init(partyId_)
    