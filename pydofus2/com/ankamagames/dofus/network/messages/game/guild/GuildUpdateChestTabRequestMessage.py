from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.inventory.UpdatedStorageTabInformation import (
        UpdatedStorageTabInformation,
    )


class GuildUpdateChestTabRequestMessage(NetworkMessage):
    tab: "UpdatedStorageTabInformation"

    def init(self, tab_: "UpdatedStorageTabInformation"):
        self.tab = tab_

        super().__init__()
