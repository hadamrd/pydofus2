from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeCraftResultMessage import (
    ExchangeCraftResultMessage,
)


class ExchangeCraftResultWithObjectIdMessage(ExchangeCraftResultMessage):
    objectGenericId: int

    def init(self, objectGenericId_: int, craftResult_: int):
        self.objectGenericId = objectGenericId_

        super().init(craftResult_)
