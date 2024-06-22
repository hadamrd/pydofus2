from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import (
    AbstractPartyMessage,
)


class PartyFollowMemberRequestMessage(AbstractPartyMessage):
    playerId: int

    def init(self, playerId_: int, partyId_: int):
        self.playerId = playerId_

        super().init(partyId_)
