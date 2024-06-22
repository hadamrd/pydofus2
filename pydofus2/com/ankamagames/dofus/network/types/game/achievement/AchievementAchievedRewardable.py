from pydofus2.com.ankamagames.dofus.network.types.game.achievement.AchievementAchieved import AchievementAchieved


class AchievementAchievedRewardable(AchievementAchieved):
    finishedLevel: int

    def init(self, finishedLevel_: int, id_: int, achievedBy_: int, achievedPioneerRank_: int):
        self.finishedLevel = finishedLevel_

        super().init(id_, achievedBy_, achievedPioneerRank_)
