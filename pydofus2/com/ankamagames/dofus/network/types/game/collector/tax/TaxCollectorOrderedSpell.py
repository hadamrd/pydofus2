from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class TaxCollectorOrderedSpell(NetworkMessage):
    spellId: int
    slot: int

    def init(self, spellId_: int, slot_: int):
        self.spellId = spellId_
        self.slot = slot_

        super().__init__()
