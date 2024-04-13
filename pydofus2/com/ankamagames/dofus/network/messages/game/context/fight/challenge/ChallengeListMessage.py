from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.challenge.ChallengeInformation import (
        ChallengeInformation,
    )


class ChallengeListMessage(NetworkMessage):
    challengesInformation: list["ChallengeInformation"]

    def init(self, challengesInformation_: list["ChallengeInformation"]):
        self.challengesInformation = challengesInformation_

        super().__init__()
