from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.ActorOrientation import \
        ActorOrientation


class GameMapChangeOrientationsMessage(NetworkMessage):
    orientations: list["ActorOrientation"]

    def init(self, orientations_: list["ActorOrientation"]):
        self.orientations = orientations_

        super().__init__()
