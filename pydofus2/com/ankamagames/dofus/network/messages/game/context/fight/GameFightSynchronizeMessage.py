from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
        GameFightFighterInformations


class GameFightSynchronizeMessage(NetworkMessage):
    fighters: list["GameFightFighterInformations"]

    def init(self, fighters_: list["GameFightFighterInformations"]):
        self.fighters = fighters_

        super().__init__()
