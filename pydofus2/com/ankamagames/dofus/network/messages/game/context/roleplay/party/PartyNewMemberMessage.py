from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyUpdateMessage import \
    PartyUpdateMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.PartyMemberInformations import \
        PartyMemberInformations


class PartyNewMemberMessage(PartyUpdateMessage):
    def init(self, memberInformations_: "PartyMemberInformations", partyId_: int):

        super().init(memberInformations_, partyId_)
