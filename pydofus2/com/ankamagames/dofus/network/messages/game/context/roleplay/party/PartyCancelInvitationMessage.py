from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import (
    AbstractPartyMessage,
)


class PartyCancelInvitationMessage(AbstractPartyMessage):
    guestId: int

    def init(self, guestId_: int, partyId_: int):
        self.guestId = guestId_

        super().init(partyId_)
