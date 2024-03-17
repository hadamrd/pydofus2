from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMessage import \
    ExchangeObjectMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem
    

class ExchangeObjectAddedMessage(ExchangeObjectMessage):
    object: 'ObjectItem'
    def init(self, object_: 'ObjectItem', remote_: bool):
        self.object = object_
        
        super().init(remote_)
    