from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class AchievementPioneerRank(NetworkMessage):
    achievementId: int
    pioneerRank: int

    def init(self, achievementId_: int, pioneerRank_: int):
        self.achievementId = achievementId_
        self.pioneerRank = pioneerRank_

        super().__init__()
