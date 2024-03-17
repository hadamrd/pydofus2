from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class TaxCollectorHarvestedMessage(NetworkMessage):
    taxCollectorId: int
    harvesterId: int
    harvesterName: str
    def init(self, taxCollectorId_: int, harvesterId_: int, harvesterName_: str):
        self.taxCollectorId = taxCollectorId_
        self.harvesterId = harvesterId_
        self.harvesterName = harvesterName_
        
        super().__init__()
    