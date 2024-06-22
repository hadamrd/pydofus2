from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import (
        AllianceInformation,
    )


class AllianceApplicationIsAnsweredMessage(NetworkMessage):
    accepted: bool
    allianceInformation: "AllianceInformation"

    def init(self, accepted_: bool, allianceInformation_: "AllianceInformation"):
        self.accepted = accepted_
        self.allianceInformation = allianceInformation_

        super().__init__()
