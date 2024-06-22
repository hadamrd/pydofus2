from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import (
    AbstractPartyMessage,
)


class PartyInvitationCancelledForGuestMessage(AbstractPartyMessage):
    cancelerId: int

    def init(self, cancelerId_: int, partyId_: int):
        self.cancelerId = cancelerId_

        super().init(partyId_)
