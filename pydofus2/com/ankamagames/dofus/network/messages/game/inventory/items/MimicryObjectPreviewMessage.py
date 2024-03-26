from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem


class MimicryObjectPreviewMessage(NetworkMessage):
    result: "ObjectItem"

    def init(self, result_: "ObjectItem"):
        self.result = result_

        super().__init__()
