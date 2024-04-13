from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import (
        AllianceInformation,
    )


class AllianceJoinedMessage(NetworkMessage):
    allianceInfo: "AllianceInformation"
    rankId: int

    def init(self, allianceInfo_: "AllianceInformation", rankId_: int):
        self.allianceInfo = allianceInfo_
        self.rankId = rankId_

        super().__init__()
