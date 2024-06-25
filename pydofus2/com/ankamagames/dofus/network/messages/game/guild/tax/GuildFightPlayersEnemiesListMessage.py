from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalPlusLookInformations import (
        CharacterMinimalPlusLookInformations,
    )


class GuildFightPlayersEnemiesListMessage(NetworkMessage):
    fightId: int
    playerInfo: list["CharacterMinimalPlusLookInformations"]

    def init(self, fightId_: int, playerInfo_: list["CharacterMinimalPlusLookInformations"]):
        self.fightId = fightId_
        self.playerInfo = playerInfo_

        super().__init__()
