from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class TaxCollectorRemovedMessage(NetworkMessage):
    collectorId: int

    def init(self, collectorId_: int):
        self.collectorId = collectorId_

        super().__init__()
