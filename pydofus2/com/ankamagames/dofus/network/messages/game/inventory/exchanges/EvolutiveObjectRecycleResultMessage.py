from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.inventory.exchanges.RecycledItem import \
        RecycledItem


class EvolutiveObjectRecycleResultMessage(NetworkMessage):
    recycledItems: list["RecycledItem"]

    def init(self, recycledItems_: list["RecycledItem"]):
        self.recycledItems = recycledItems_

        super().__init__()
