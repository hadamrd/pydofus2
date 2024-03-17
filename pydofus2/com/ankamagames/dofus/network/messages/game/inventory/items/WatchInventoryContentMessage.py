from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.InventoryContentMessage import \
    InventoryContentMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem
    

class WatchInventoryContentMessage(InventoryContentMessage):
    def init(self, objects_: list['ObjectItem'], kamas_: int):
        
        super().init(objects_, kamas_)
    