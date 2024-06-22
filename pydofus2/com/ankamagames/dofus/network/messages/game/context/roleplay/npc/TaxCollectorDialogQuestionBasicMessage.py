from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicAllianceInformations import (
        BasicAllianceInformations,
    )


class TaxCollectorDialogQuestionBasicMessage(NetworkMessage):
    allianceInfo: "BasicAllianceInformations"

    def init(self, allianceInfo_: "BasicAllianceInformations"):
        self.allianceInfo = allianceInfo_

        super().__init__()
