from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSell import \
    ObjectItemToSell

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import \
        ObjectEffect
    

class ObjectItemToSellInBid(ObjectItemToSell):
    unsoldDelay: int
    def init(self, unsoldDelay_: int, objectGID_: int, effects_: list['ObjectEffect'], objectUID_: int, quantity_: int, objectPrice_: int):
        self.unsoldDelay = unsoldDelay_
        
        super().init(objectGID_, effects_, objectUID_, quantity_, objectPrice_)
    