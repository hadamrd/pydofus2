from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class FightLootObject(NetworkMessage):
    objectId: int
    quantity: int
    priorityHint: int

    def init(self, objectId_: int, quantity_: int, priorityHint_: int):
        self.objectId = objectId_
        self.quantity = quantity_
        self.priorityHint = priorityHint_

        super().__init__()
