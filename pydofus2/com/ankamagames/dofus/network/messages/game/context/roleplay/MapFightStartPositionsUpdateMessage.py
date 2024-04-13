from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightStartingPositions import (
        FightStartingPositions,
    )


class MapFightStartPositionsUpdateMessage(NetworkMessage):
    mapId: int
    fightStartPositions: "FightStartingPositions"

    def init(self, mapId_: int, fightStartPositions_: "FightStartingPositions"):
        self.mapId = mapId_
        self.fightStartPositions = fightStartPositions_

        super().__init__()
