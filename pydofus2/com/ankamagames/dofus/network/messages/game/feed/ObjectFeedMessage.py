from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemQuantity import ObjectItemQuantity


class ObjectFeedMessage(NetworkMessage):
    objectUID: int
    meal: list["ObjectItemQuantity"]

    def init(self, objectUID_: int, meal_: list["ObjectItemQuantity"]):
        self.objectUID = objectUID_
        self.meal = meal_

        super().__init__()
