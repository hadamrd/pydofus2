from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorInformations import \
        TaxCollectorInformations


class TopTaxCollectorListMessage(NetworkMessage):
    dungeonTaxCollectorsInformation: list["TaxCollectorInformations"]
    worldTaxCollectorsInformation: list["TaxCollectorInformations"]

    def init(
        self,
        dungeonTaxCollectorsInformation_: list["TaxCollectorInformations"],
        worldTaxCollectorsInformation_: list["TaxCollectorInformations"],
    ):
        self.dungeonTaxCollectorsInformation = dungeonTaxCollectorsInformation_
        self.worldTaxCollectorsInformation = worldTaxCollectorsInformation_

        super().__init__()
