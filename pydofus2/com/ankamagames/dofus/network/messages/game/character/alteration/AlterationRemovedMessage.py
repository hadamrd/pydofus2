from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.alteration.AlterationInfo import \
        AlterationInfo


class AlterationRemovedMessage(NetworkMessage):
    alteration: "AlterationInfo"

    def init(self, alteration_: "AlterationInfo"):
        self.alteration = alteration_

        super().__init__()
