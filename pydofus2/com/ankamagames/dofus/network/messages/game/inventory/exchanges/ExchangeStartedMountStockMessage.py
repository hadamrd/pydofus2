from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import ObjectItem


class ExchangeStartedMountStockMessage(NetworkMessage):
    objectsInfos: list["ObjectItem"]

    def init(self, objectsInfos_: list["ObjectItem"]):
        self.objectsInfos = objectsInfos_

        super().__init__()
