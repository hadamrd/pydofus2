from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.mount.MountClientData import \
        MountClientData


class ExchangeMountsStableAddMessage(NetworkMessage):
    mountDescription: list["MountClientData"]

    def init(self, mountDescription_: list["MountClientData"]):
        self.mountDescription = mountDescription_

        super().__init__()
