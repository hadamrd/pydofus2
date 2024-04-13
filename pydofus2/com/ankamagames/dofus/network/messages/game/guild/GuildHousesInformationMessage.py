from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInformationsForGuild import (
        HouseInformationsForGuild,
    )


class GuildHousesInformationMessage(NetworkMessage):
    housesInformations: list["HouseInformationsForGuild"]

    def init(self, housesInformations_: list["HouseInformationsForGuild"]):
        self.housesInformations = housesInformations_

        super().__init__()
