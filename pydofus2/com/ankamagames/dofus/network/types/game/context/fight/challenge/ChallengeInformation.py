from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.challenge.ChallengeTargetInformation import (
        ChallengeTargetInformation,
    )


class ChallengeInformation(NetworkMessage):
    challengeId: int
    targetsList: list["ChallengeTargetInformation"]
    dropBonus: int
    xpBonus: int
    state: int

    def init(
        self,
        challengeId_: int,
        targetsList_: list["ChallengeTargetInformation"],
        dropBonus_: int,
        xpBonus_: int,
        state_: int,
    ):
        self.challengeId = challengeId_
        self.targetsList = targetsList_
        self.dropBonus = dropBonus_
        self.xpBonus = xpBonus_
        self.state = state_

        super().__init__()
