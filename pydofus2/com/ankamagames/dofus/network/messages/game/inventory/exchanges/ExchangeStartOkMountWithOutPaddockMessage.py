from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.mount.MountClientData import \
        MountClientData


class ExchangeStartOkMountWithOutPaddockMessage(NetworkMessage):
    stabledMountsDescription: list["MountClientData"]

    def init(self, stabledMountsDescription_: list["MountClientData"]):
        self.stabledMountsDescription = stabledMountsDescription_

        super().__init__()
