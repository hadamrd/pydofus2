from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.data.items.Item import Item

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import ObjectEffect


class ObjectItem(Item):
    position: int
    objectGID: int
    effects: list["ObjectEffect"]
    objectUID: int
    quantity: int
    favorite: bool

    def init(
        self,
        position_: int,
        objectGID_: int,
        effects_: list["ObjectEffect"],
        objectUID_: int,
        quantity_: int,
        favorite_: bool,
    ):
        self.position = position_
        self.objectGID = objectGID_
        self.effects = effects_
        self.objectUID = objectUID_
        self.quantity = quantity_
        self.favorite = favorite_

        super().init()
