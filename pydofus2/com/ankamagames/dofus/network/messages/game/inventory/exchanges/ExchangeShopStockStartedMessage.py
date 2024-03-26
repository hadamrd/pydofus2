from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSell import \
        ObjectItemToSell


class ExchangeShopStockStartedMessage(NetworkMessage):
    objectsInfos: list["ObjectItemToSell"]

    def init(self, objectsInfos_: list["ObjectItemToSell"]):
        self.objectsInfos = objectsInfos_

        super().__init__()
