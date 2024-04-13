from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.mount.MountClientData import MountClientData


class MountSetMessage(NetworkMessage):
    mountData: "MountClientData"

    def init(self, mountData_: "MountClientData"):
        self.mountData = mountData_

        super().__init__()
