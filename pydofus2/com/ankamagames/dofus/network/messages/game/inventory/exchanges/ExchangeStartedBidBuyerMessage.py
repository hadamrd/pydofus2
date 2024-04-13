from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.SellerBuyerDescriptor import (
        SellerBuyerDescriptor,
    )


class ExchangeStartedBidBuyerMessage(NetworkMessage):
    buyerDescriptor: "SellerBuyerDescriptor"

    def init(self, buyerDescriptor_: "SellerBuyerDescriptor"):
        self.buyerDescriptor = buyerDescriptor_

        super().__init__()
