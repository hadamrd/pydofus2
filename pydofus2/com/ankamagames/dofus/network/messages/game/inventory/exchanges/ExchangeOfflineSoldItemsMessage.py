from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemQuantityPriceDateEffects import \
        ObjectItemQuantityPriceDateEffects


class ExchangeOfflineSoldItemsMessage(NetworkMessage):
    bidHouseItems: list["ObjectItemQuantityPriceDateEffects"]

    def init(self, bidHouseItems_: list["ObjectItemQuantityPriceDateEffects"]):
        self.bidHouseItems = bidHouseItems_

        super().__init__()
