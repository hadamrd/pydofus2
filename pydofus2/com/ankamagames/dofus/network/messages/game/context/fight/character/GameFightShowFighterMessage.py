from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
        GameFightFighterInformations


class GameFightShowFighterMessage(NetworkMessage):
    informations: "GameFightFighterInformations"

    def init(self, informations_: "GameFightFighterInformations"):
        self.informations = informations_

        super().__init__()
