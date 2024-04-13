from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterInGroupLightInformations import (
        MonsterInGroupLightInformations,
    )


class AlternativeMonstersInGroupLightInformations(NetworkMessage):
    playerCount: int
    monsters: list["MonsterInGroupLightInformations"]

    def init(self, playerCount_: int, monsters_: list["MonsterInGroupLightInformations"]):
        self.playerCount = playerCount_
        self.monsters = monsters_

        super().__init__()
