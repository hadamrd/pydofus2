from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import \
        InteractiveElement


class InteractiveMapUpdateMessage(NetworkMessage):
    interactiveElements: list["InteractiveElement"]

    def init(self, interactiveElements_: list["InteractiveElement"]):
        self.interactiveElements = interactiveElements_

        super().__init__()
