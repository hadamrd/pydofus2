from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSell import \
        ObjectItemToSell


class ExchangeShopStockMultiMovementUpdatedMessage(NetworkMessage):
    objectInfoList: list["ObjectItemToSell"]

    def init(self, objectInfoList_: list["ObjectItemToSell"]):
        self.objectInfoList = objectInfoList_

        super().__init__()
