from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.paddock.PaddockInstancesInformations import (
        PaddockInstancesInformations,
    )


class PaddockPropertiesMessage(NetworkMessage):
    properties: "PaddockInstancesInformations"

    def init(self, properties_: "PaddockInstancesInformations"):
        self.properties = properties_

        super().__init__()
