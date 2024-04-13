from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamInformations import (
        FightTeamInformations,
    )


class GameFightUpdateTeamMessage(NetworkMessage):
    fightId: int
    team: "FightTeamInformations"

    def init(self, fightId_: int, team_: "FightTeamInformations"):
        self.fightId = fightId_
        self.team = team_

        super().__init__()
