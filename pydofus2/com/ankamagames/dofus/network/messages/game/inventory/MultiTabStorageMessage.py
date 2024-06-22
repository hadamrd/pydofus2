from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.inventory.StorageTabInformation import StorageTabInformation


class MultiTabStorageMessage(NetworkMessage):
    tabs: list["StorageTabInformation"]

    def init(self, tabs_: list["StorageTabInformation"]):
        self.tabs = tabs_

        super().__init__()
