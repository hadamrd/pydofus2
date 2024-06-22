from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ExchangeObjectMoveToTabMessage(NetworkMessage):
    objectUID: int
    quantity: int
    tabNumber: int

    def init(self, objectUID_: int, quantity_: int, tabNumber_: int):
        self.objectUID = objectUID_
        self.quantity = quantity_
        self.tabNumber = tabNumber_

        super().__init__()
