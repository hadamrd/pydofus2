from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkMountWithOutPaddockMessage import (
    ExchangeStartOkMountWithOutPaddockMessage,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.mount.MountClientData import MountClientData


class ExchangeStartOkMountMessage(ExchangeStartOkMountWithOutPaddockMessage):
    paddockedMountsDescription: list["MountClientData"]

    def init(
        self, paddockedMountsDescription_: list["MountClientData"], stabledMountsDescription_: list["MountClientData"]
    ):
        self.paddockedMountsDescription = paddockedMountsDescription_

        super().init(stabledMountsDescription_)
