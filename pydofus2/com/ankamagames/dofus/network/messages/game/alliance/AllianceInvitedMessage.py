from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import \
        AllianceInformation


class AllianceInvitedMessage(NetworkMessage):
    recruterName: str
    allianceInfo: "AllianceInformation"

    def init(self, recruterName_: str, allianceInfo_: "AllianceInformation"):
        self.recruterName = recruterName_
        self.allianceInfo = allianceInfo_

        super().__init__()
