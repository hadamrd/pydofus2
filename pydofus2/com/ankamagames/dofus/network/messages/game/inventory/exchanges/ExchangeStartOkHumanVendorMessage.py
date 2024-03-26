from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSellInHumanVendorShop import \
        ObjectItemToSellInHumanVendorShop


class ExchangeStartOkHumanVendorMessage(NetworkMessage):
    sellerId: int
    objectsInfos: list["ObjectItemToSellInHumanVendorShop"]

    def init(self, sellerId_: int, objectsInfos_: list["ObjectItemToSellInHumanVendorShop"]):
        self.sellerId = sellerId_
        self.objectsInfos = objectsInfos_

        super().__init__()
