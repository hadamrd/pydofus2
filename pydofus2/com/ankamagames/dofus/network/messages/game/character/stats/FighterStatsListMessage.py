from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicsInformations import (
        CharacterCharacteristicsInformations,
    )


class FighterStatsListMessage(NetworkMessage):
    stats: "CharacterCharacteristicsInformations"

    def init(self, stats_: "CharacterCharacteristicsInformations"):
        self.stats = stats_

        super().__init__()
