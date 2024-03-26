from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.PartyInvitationRequestMessage import \
    PartyInvitationRequestMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AbstractPlayerSearchInformation import \
        AbstractPlayerSearchInformation


class PartyInvitationArenaRequestMessage(PartyInvitationRequestMessage):
    def init(self, target_: "AbstractPlayerSearchInformation"):

        super().init(target_)
