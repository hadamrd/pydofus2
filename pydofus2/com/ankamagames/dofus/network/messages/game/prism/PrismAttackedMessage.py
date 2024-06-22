from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.prism.PrismGeolocalizedInformation import (
        PrismGeolocalizedInformation,
    )


class PrismAttackedMessage(NetworkMessage):
    prism: "PrismGeolocalizedInformation"

    def init(self, prism_: "PrismGeolocalizedInformation"):
        self.prism = prism_

        super().__init__()
