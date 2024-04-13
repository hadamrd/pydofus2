from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemQuantity import ObjectItemQuantity


class ObjectsQuantityMessage(NetworkMessage):
    objectsUIDAndQty: list["ObjectItemQuantity"]

    def init(self, objectsUIDAndQty_: list["ObjectItemQuantity"]):
        self.objectsUIDAndQty = objectsUIDAndQty_

        super().__init__()
