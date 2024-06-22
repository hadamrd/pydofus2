from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import (
    AbstractPartyMessage,
)


class PartyDeletedMessage(AbstractPartyMessage):
    def init(self, partyId_: int):

        super().init(partyId_)
