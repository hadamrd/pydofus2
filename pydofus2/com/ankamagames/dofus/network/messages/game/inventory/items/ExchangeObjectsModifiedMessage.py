from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMessage import \
    ExchangeObjectMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem
    

class ExchangeObjectsModifiedMessage(ExchangeObjectMessage):
    object: list['ObjectItem']
    def init(self, object_: list['ObjectItem'], remote_: bool):
        self.object = object_
        
        super().init(remote_)
    