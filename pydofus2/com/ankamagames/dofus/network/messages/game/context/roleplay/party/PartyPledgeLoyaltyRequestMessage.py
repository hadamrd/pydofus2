from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import (
    AbstractPartyMessage,
)


class PartyPledgeLoyaltyRequestMessage(AbstractPartyMessage):
    loyal: bool

    def init(self, loyal_: bool, partyId_: int):
        self.loyal = loyal_

        super().init(partyId_)
