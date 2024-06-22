from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedMessage import (
    ExchangeStartedMessage,
)


class ExchangeStartedWithStorageMessage(ExchangeStartedMessage):
    storageMaxSlot: int

    def init(self, storageMaxSlot_: int, exchangeType_: int):
        self.storageMaxSlot = storageMaxSlot_

        super().init(exchangeType_)
