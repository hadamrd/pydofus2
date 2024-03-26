from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.achievement.AchievementPioneerRank import \
        AchievementPioneerRank


class AchievementsPioneerRanksMessage(NetworkMessage):
    achievementsPioneerRanks: list["AchievementPioneerRank"]

    def init(self, achievementsPioneerRanks_: list["AchievementPioneerRank"]):
        self.achievementsPioneerRanks = achievementsPioneerRanks_

        super().__init__()
