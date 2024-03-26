from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.achievement.AchievementAchieved import \
        AchievementAchieved


class AchievementListMessage(NetworkMessage):
    finishedAchievements: list["AchievementAchieved"]

    def init(self, finishedAchievements_: list["AchievementAchieved"]):
        self.finishedAchievements = finishedAchievements_

        super().__init__()
