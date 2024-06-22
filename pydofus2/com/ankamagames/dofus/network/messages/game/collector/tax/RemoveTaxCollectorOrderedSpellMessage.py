from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class RemoveTaxCollectorOrderedSpellMessage(NetworkMessage):
    taxCollectorId: int
    slot: int

    def init(self, taxCollectorId_: int, slot_: int):
        self.taxCollectorId = taxCollectorId_
        self.slot = slot_

        super().__init__()
