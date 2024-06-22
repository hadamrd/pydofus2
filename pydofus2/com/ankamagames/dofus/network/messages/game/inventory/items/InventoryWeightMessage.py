from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class InventoryWeightMessage(NetworkMessage):
    inventoryWeight: int
    weightMax: int

    def init(self, inventoryWeight_: int, weightMax_: int):
        self.inventoryWeight = inventoryWeight_
        self.weightMax = weightMax_

        super().__init__()
