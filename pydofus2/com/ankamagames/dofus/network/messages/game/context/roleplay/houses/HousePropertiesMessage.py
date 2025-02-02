from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInstanceInformations import (
        HouseInstanceInformations,
    )


class HousePropertiesMessage(NetworkMessage):
    houseId: int
    doorsOnMap: list[int]
    properties: "HouseInstanceInformations"

    def init(self, houseId_: int, doorsOnMap_: list[int], properties_: "HouseInstanceInformations"):
        self.houseId = houseId_
        self.doorsOnMap = doorsOnMap_
        self.properties = properties_

        super().__init__()
