from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyEventMessage import (
    AbstractPartyEventMessage,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyMemberInformations import (
        PartyMemberInformations,
    )


class PartyUpdateMessage(AbstractPartyEventMessage):
    memberInformations: "PartyMemberInformations"

    def init(self, memberInformations_: "PartyMemberInformations", partyId_: int):
        self.memberInformations = memberInformations_

        super().init(partyId_)
