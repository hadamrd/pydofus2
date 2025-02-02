from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.friend.FriendInformations import FriendInformations


class FriendUpdateMessage(NetworkMessage):
    friendUpdated: "FriendInformations"

    def init(self, friendUpdated_: "FriendInformations"):
        self.friendUpdated = friendUpdated_

        super().__init__()
