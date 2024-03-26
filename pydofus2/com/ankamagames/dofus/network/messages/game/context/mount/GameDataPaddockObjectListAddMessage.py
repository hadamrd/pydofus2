from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.paddock.PaddockItem import \
        PaddockItem


class GameDataPaddockObjectListAddMessage(NetworkMessage):
    paddockItemDescription: list["PaddockItem"]

    def init(self, paddockItemDescription_: list["PaddockItem"]):
        self.paddockItemDescription = paddockItemDescription_

        super().__init__()
