from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.startup.GameActionItem import GameActionItem


class GameActionItemAddMessage(NetworkMessage):
    newAction: "GameActionItem"

    def init(self, newAction_: "GameActionItem"):
        self.newAction = newAction_

        super().__init__()
