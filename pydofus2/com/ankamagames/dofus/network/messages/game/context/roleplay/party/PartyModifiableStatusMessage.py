from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import (
    AbstractPartyMessage,
)


class PartyModifiableStatusMessage(AbstractPartyMessage):
    enabled: bool

    def init(self, enabled_: bool, partyId_: int):
        self.enabled = enabled_

        super().init(partyId_)
