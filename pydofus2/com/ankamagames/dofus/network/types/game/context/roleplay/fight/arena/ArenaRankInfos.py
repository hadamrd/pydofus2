from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.fight.arena.ArenaLeagueRanking import \
        ArenaLeagueRanking


class ArenaRankInfos(NetworkMessage):
    arenaType: int
    leagueRanking: "ArenaLeagueRanking"
    bestLeagueId: int
    bestRating: int
    dailyVictoryCount: int
    seasonVictoryCount: int
    dailyFightcount: int
    seasonFightcount: int
    numFightNeededForLadder: int

    def init(
        self,
        arenaType_: int,
        leagueRanking_: "ArenaLeagueRanking",
        bestLeagueId_: int,
        bestRating_: int,
        dailyVictoryCount_: int,
        seasonVictoryCount_: int,
        dailyFightcount_: int,
        seasonFightcount_: int,
        numFightNeededForLadder_: int,
    ):
        self.arenaType = arenaType_
        self.leagueRanking = leagueRanking_
        self.bestLeagueId = bestLeagueId_
        self.bestRating = bestRating_
        self.dailyVictoryCount = dailyVictoryCount_
        self.seasonVictoryCount = seasonVictoryCount_
        self.dailyFightcount = dailyFightcount_
        self.seasonFightcount = seasonFightcount_
        self.numFightNeededForLadder = numFightNeededForLadder_

        super().__init__()
