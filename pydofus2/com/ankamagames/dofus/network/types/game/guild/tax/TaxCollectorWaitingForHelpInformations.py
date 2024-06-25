from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.guild.tax.TaxCollectorComplementaryInformations import (
    TaxCollectorComplementaryInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.fight.ProtectedEntityWaitingForHelpInfo import (
        ProtectedEntityWaitingForHelpInfo,
    )


class TaxCollectorWaitingForHelpInformations(TaxCollectorComplementaryInformations):
    waitingForHelpInfo: "ProtectedEntityWaitingForHelpInfo"

    def init(self, waitingForHelpInfo_: "ProtectedEntityWaitingForHelpInfo"):
        self.waitingForHelpInfo = waitingForHelpInfo_

        super().init()
