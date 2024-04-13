from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInformations import HouseInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInstanceInformations import (
        HouseInstanceInformations,
    )


class AccountHouseInformations(HouseInformations):
    houseInfos: "HouseInstanceInformations"
    worldX: int
    worldY: int
    mapId: int
    subAreaId: int

    def init(
        self,
        houseInfos_: "HouseInstanceInformations",
        worldX_: int,
        worldY_: int,
        mapId_: int,
        subAreaId_: int,
        houseId_: int,
        modelId_: int,
    ):
        self.houseInfos = houseInfos_
        self.worldX = worldX_
        self.worldY = worldY_
        self.mapId = mapId_
        self.subAreaId = subAreaId_

        super().init(houseId_, modelId_)
