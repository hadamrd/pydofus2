from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterLightInformations import \
        GameFightFighterLightInformations


class MapRunningFightDetailsMessage(NetworkMessage):
    fightId: int
    attackers: list["GameFightFighterLightInformations"]
    defenders: list["GameFightFighterLightInformations"]

    def init(
        self,
        fightId_: int,
        attackers_: list["GameFightFighterLightInformations"],
        defenders_: list["GameFightFighterLightInformations"],
    ):
        self.fightId = fightId_
        self.attackers = attackers_
        self.defenders = defenders_

        super().__init__()
