from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.data.items.Item import \
    Item

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import \
        ObjectEffect
    

class ObjectItemToSellInHumanVendorShop(Item):
    objectGID: int
    effects: list['ObjectEffect']
    objectUID: int
    quantity: int
    objectPrice: int
    publicPrice: int
    def init(self, objectGID_: int, effects_: list['ObjectEffect'], objectUID_: int, quantity_: int, objectPrice_: int, publicPrice_: int):
        self.objectGID = objectGID_
        self.effects = effects_
        self.objectUID = objectUID_
        self.quantity = quantity_
        self.objectPrice = objectPrice_
        self.publicPrice = publicPrice_
        
        super().init()
    