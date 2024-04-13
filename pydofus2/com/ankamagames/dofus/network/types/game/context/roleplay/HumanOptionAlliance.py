from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOption import HumanOption

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import (
        AllianceInformation,
    )


class HumanOptionAlliance(HumanOption):
    allianceInformation: "AllianceInformation"
    aggressable: int

    def init(self, allianceInformation_: "AllianceInformation", aggressable_: int):
        self.allianceInformation = allianceInformation_
        self.aggressable = aggressable_

        super().init()
