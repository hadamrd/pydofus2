from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.havenbag.HavenBagRoomPreviewInformation import (
        HavenBagRoomPreviewInformation,
    )


class HavenBagRoomUpdateMessage(NetworkMessage):
    action: int
    roomsPreview: list["HavenBagRoomPreviewInformation"]

    def init(self, action_: int, roomsPreview_: list["HavenBagRoomPreviewInformation"]):
        self.action = action_
        self.roomsPreview = roomsPreview_

        super().__init__()
