from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class MoveTaxCollectorOrderedSpellMessage(NetworkMessage):
    taxCollectorId: int
    movedFrom: int
    movedTo: int

    def init(self, taxCollectorId_: int, movedFrom_: int, movedTo_: int):
        self.taxCollectorId = taxCollectorId_
        self.movedFrom = movedFrom_
        self.movedTo = movedTo_

        super().__init__()
