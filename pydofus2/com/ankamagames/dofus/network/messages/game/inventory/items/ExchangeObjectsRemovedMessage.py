from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMessage import (
    ExchangeObjectMessage,
)


class ExchangeObjectsRemovedMessage(ExchangeObjectMessage):
    objectUID: list[int]

    def init(self, objectUID_: list[int], remote_: bool):
        self.objectUID = objectUID_

        super().init(remote_)
