from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.interactive.StatedElement import StatedElement


class StatedElementUpdatedMessage(NetworkMessage):
    statedElement: "StatedElement"

    def init(self, statedElement_: "StatedElement"):
        self.statedElement = statedElement_

        super().__init__()
