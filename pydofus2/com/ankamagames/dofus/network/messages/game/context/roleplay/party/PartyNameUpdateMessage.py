from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import (
    AbstractPartyMessage,
)


class PartyNameUpdateMessage(AbstractPartyMessage):
    partyName: str

    def init(self, partyName_: str, partyId_: int):
        self.partyName = partyName_

        super().init(partyId_)
