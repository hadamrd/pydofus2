from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemMinimalInformation import \
    ObjectItemMinimalInformation

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import \
        ObjectEffect


class ObjectItemToSellInNpcShop(ObjectItemMinimalInformation):
    objectPrice: int
    buyCriterion: str

    def init(self, objectPrice_: int, buyCriterion_: str, objectGID_: int, effects_: list["ObjectEffect"]):
        self.objectPrice = objectPrice_
        self.buyCriterion = buyCriterion_

        super().init(objectGID_, effects_)
