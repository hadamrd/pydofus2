from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AtlasPointsInformations import \
        AtlasPointsInformations


class AtlasPointInformationsMessage(NetworkMessage):
    type: "AtlasPointsInformations"

    def init(self, type_: "AtlasPointsInformations"):
        self.type = type_

        super().__init__()
