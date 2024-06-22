from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSellInBid import (
        ObjectItemToSellInBid,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.SellerBuyerDescriptor import (
        SellerBuyerDescriptor,
    )


class ExchangeStartedBidSellerMessage(NetworkMessage):
    sellerDescriptor: "SellerBuyerDescriptor"
    objectsInfos: list["ObjectItemToSellInBid"]

    def init(self, sellerDescriptor_: "SellerBuyerDescriptor", objectsInfos_: list["ObjectItemToSellInBid"]):
        self.sellerDescriptor = sellerDescriptor_
        self.objectsInfos = objectsInfos_

        super().__init__()
