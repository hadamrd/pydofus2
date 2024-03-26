from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.prism.PrismInformation import \
    PrismInformation

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import \
        AllianceInformation


class AlliancePrismInformation(PrismInformation):
    alliance: "AllianceInformation"

    def init(
        self,
        alliance_: "AllianceInformation",
        state_: int,
        placementDate_: int,
        nuggetsCount_: int,
        durability_: int,
        nextEvolutionDate_: int,
    ):
        self.alliance = alliance_

        super().init(state_, placementDate_, nuggetsCount_, durability_, nextEvolutionDate_)
