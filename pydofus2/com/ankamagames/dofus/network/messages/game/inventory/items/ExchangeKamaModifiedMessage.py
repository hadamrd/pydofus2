from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMessage import (
    ExchangeObjectMessage,
)


class ExchangeKamaModifiedMessage(ExchangeObjectMessage):
    quantity: int

    def init(self, quantity_: int, remote_: bool):
        self.quantity = quantity_

        super().init(remote_)
