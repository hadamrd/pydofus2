from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.friend.AbstractContactInformations import (
    AbstractContactInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import AccountTagInformation


class IgnoredInformations(AbstractContactInformations):
    def init(self, accountId_: int, accountTag_: "AccountTagInformation"):

        super().init(accountId_, accountTag_)
