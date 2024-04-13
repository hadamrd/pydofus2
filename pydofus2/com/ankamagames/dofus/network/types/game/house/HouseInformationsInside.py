from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInformations import HouseInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInstanceInformations import (
        HouseInstanceInformations,
    )


class HouseInformationsInside(HouseInformations):
    houseInfos: "HouseInstanceInformations"
    worldX: int
    worldY: int

    def init(self, houseInfos_: "HouseInstanceInformations", worldX_: int, worldY_: int, houseId_: int, modelId_: int):
        self.houseInfos = houseInfos_
        self.worldX = worldX_
        self.worldY = worldY_

        super().init(houseId_, modelId_)
