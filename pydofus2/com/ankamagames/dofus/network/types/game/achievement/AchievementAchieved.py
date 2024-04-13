from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class AchievementAchieved(NetworkMessage):
    id: int
    achievedBy: int
    achievedPioneerRank: int

    def init(self, id_: int, achievedBy_: int, achievedPioneerRank_: int):
        self.id = id_
        self.achievedBy = achievedBy_
        self.achievedPioneerRank = achievedPioneerRank_

        super().__init__()
