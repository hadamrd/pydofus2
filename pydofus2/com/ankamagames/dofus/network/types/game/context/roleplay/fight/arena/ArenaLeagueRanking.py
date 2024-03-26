from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class ArenaLeagueRanking(NetworkMessage):
    rating: int
    leagueId: int
    ladderPosition: int

    def init(self, rating_: int, leagueId_: int, ladderPosition_: int):
        self.rating = rating_
        self.leagueId = leagueId_
        self.ladderPosition = ladderPosition_

        super().__init__()
