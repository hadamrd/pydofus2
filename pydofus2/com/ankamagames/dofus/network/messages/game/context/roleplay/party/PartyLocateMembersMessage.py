from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import \
    AbstractPartyMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyMemberGeoPosition import \
        PartyMemberGeoPosition


class PartyLocateMembersMessage(AbstractPartyMessage):
    geopositions: list["PartyMemberGeoPosition"]

    def init(self, geopositions_: list["PartyMemberGeoPosition"], partyId_: int):
        self.geopositions = geopositions_

        super().init(partyId_)
