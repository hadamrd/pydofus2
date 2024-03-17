from pydofus2.com.ankamagames.dofus.network.types.game.achievement.AchievementAchieved import \
    AchievementAchieved


class AchievementAchievedRewardable(AchievementAchieved):
    finishedlevel: int
    def init(self, finishedlevel_: int, id_: int, achievedBy_: int):
        self.finishedlevel = finishedlevel_
        
        super().init(id_, achievedBy_)
    