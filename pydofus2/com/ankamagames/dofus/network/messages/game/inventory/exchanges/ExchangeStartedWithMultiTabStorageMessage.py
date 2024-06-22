from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedMessage import (
    ExchangeStartedMessage,
)


class ExchangeStartedWithMultiTabStorageMessage(ExchangeStartedMessage):
    storageMaxSlot: int
    tabNumber: int

    def init(self, storageMaxSlot_: int, tabNumber_: int, exchangeType_: int):
        self.storageMaxSlot = storageMaxSlot_
        self.tabNumber = tabNumber_

        super().init(exchangeType_)
