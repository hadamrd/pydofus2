from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.friend.AbstractContactInformations import \
    AbstractContactInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import \
        AccountTagInformation


class LeagueFriendInformations(AbstractContactInformations):
    playerId: int
    playerName: str
    breed: int
    sex: bool
    level: int
    leagueId: int
    totalLeaguePoints: int
    ladderPosition: int

    def init(
        self,
        playerId_: int,
        playerName_: str,
        breed_: int,
        sex_: bool,
        level_: int,
        leagueId_: int,
        totalLeaguePoints_: int,
        ladderPosition_: int,
        accountId_: int,
        accountTag_: "AccountTagInformation",
    ):
        self.playerId = playerId_
        self.playerName = playerName_
        self.breed = breed_
        self.sex = sex_
        self.level = level_
        self.leagueId = leagueId_
        self.totalLeaguePoints = totalLeaguePoints_
        self.ladderPosition = ladderPosition_

        super().init(accountId_, accountTag_)
