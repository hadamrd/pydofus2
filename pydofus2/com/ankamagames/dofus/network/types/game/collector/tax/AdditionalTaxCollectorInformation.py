from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class AdditionalTaxCollectorInformation(NetworkMessage):
    collectorCallerId: int
    collectorCallerName: str
    date: int

    def init(self, collectorCallerId_: int, collectorCallerName_: str, date_: int):
        self.collectorCallerId = collectorCallerId_
        self.collectorCallerName = collectorCallerName_
        self.date = date_

        super().__init__()
