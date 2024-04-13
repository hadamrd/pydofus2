from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMovePricedMessage import (
    ExchangeObjectMovePricedMessage,
)


class ExchangeObjectModifyPricedMessage(ExchangeObjectMovePricedMessage):
    def init(self, price_: int, objectUID_: int, quantity_: int):

        super().init(price_, objectUID_, quantity_)
