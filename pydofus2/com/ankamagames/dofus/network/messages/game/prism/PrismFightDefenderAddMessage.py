from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalPlusLookInformations import (
        CharacterMinimalPlusLookInformations,
    )


class PrismFightDefenderAddMessage(NetworkMessage):
    subAreaId: int
    fightId: int
    defender: "CharacterMinimalPlusLookInformations"

    def init(self, subAreaId_: int, fightId_: int, defender_: "CharacterMinimalPlusLookInformations"):
        self.subAreaId = subAreaId_
        self.fightId = fightId_
        self.defender = defender_

        super().__init__()
