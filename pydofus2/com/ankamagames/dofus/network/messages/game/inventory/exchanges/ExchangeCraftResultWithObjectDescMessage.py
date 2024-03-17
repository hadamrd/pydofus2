from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeCraftResultMessage import \
    ExchangeCraftResultMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemNotInContainer import \
        ObjectItemNotInContainer
    

class ExchangeCraftResultWithObjectDescMessage(ExchangeCraftResultMessage):
    objectInfo: 'ObjectItemNotInContainer'
    def init(self, objectInfo_: 'ObjectItemNotInContainer', craftResult_: int):
        self.objectInfo = objectInfo_
        
        super().init(craftResult_)
    