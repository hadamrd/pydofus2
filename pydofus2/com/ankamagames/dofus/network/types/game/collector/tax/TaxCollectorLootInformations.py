from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorComplementaryInformations import \
    TaxCollectorComplementaryInformations


class TaxCollectorLootInformations(TaxCollectorComplementaryInformations):
    pods: int
    itemsValue: int

    def init(self, pods_: int, itemsValue_: int):
        self.pods = pods_
        self.itemsValue = itemsValue_

        super().init()
