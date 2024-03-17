from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyEventMessage import \
    AbstractPartyEventMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyGuestInformations import \
        PartyGuestInformations
    

class PartyNewGuestMessage(AbstractPartyEventMessage):
    guest: 'PartyGuestInformations'
    def init(self, guest_: 'PartyGuestInformations', partyId_: int):
        self.guest = guest_
        
        super().init(partyId_)
    