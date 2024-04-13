from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.challenge.ChallengeInformation import (
        ChallengeInformation,
    )


class ChallengeTargetsMessage(NetworkMessage):
    challengeInformation: "ChallengeInformation"

    def init(self, challengeInformation_: "ChallengeInformation"):
        self.challengeInformation = challengeInformation_

        super().__init__()
