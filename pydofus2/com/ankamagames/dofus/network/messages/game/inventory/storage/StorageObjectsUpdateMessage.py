from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import ObjectItem


class StorageObjectsUpdateMessage(NetworkMessage):
    objectList: list["ObjectItem"]

    def init(self, objectList_: list["ObjectItem"]):
        self.objectList = objectList_

        super().__init__()
