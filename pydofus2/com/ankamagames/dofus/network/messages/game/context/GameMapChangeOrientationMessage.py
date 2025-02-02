from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.ActorOrientation import ActorOrientation


class GameMapChangeOrientationMessage(NetworkMessage):
    orientation: "ActorOrientation"

    def init(self, orientation_: "ActorOrientation"):
        self.orientation = orientation_

        super().__init__()
