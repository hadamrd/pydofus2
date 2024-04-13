from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.friend.AbstractContactInformations import (
    AbstractContactInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import AccountTagInformation


class AcquaintanceInformation(AbstractContactInformations):
    playerState: int

    def init(self, playerState_: int, accountId_: int, accountTag_: "AccountTagInformation"):
        self.playerState = playerState_

        super().init(accountId_, accountTag_)
