from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.challenge.ChallengeTargetInformation import \
    ChallengeTargetInformation


class ChallengeTargetWithAttackerInformation(ChallengeTargetInformation):
    attackersIds: list[int]

    def init(self, attackersIds_: list[int], targetId_: int, targetCell_: int):
        self.attackersIds = attackersIds_

        super().init(targetId_, targetCell_)
