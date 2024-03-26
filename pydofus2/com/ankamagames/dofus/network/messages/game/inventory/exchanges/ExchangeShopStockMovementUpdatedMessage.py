from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSell import \
        ObjectItemToSell


class ExchangeShopStockMovementUpdatedMessage(NetworkMessage):
    objectInfo: "ObjectItemToSell"

    def init(self, objectInfo_: "ObjectItemToSell"):
        self.objectInfo = objectInfo_

        super().__init__()
