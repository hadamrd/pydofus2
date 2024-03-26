from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.alliance.AllianceJoinedMessage import \
    AllianceJoinedMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import \
        AllianceInformation


class AllianceMembershipMessage(AllianceJoinedMessage):
    def init(self, allianceInfo_: "AllianceInformation", rankId_: int):

        super().init(allianceInfo_, rankId_)
