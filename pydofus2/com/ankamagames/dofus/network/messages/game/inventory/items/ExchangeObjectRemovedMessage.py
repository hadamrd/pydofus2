from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMessage import (
    ExchangeObjectMessage,
)


class ExchangeObjectRemovedMessage(ExchangeObjectMessage):
    objectUID: int

    def init(self, objectUID_: int, remote_: bool):
        self.objectUID = objectUID_

        super().init(remote_)
