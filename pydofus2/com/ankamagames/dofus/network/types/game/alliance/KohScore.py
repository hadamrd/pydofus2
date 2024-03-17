from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class KohScore(NetworkMessage):
    avaScoreTypeEnum: int
    roundScores: int
    cumulScores: int
    def init(self, avaScoreTypeEnum_: int, roundScores_: int, cumulScores_: int):
        self.avaScoreTypeEnum = avaScoreTypeEnum_
        self.roundScores = roundScores_
        self.cumulScores = cumulScores_
        
        super().__init__()
    