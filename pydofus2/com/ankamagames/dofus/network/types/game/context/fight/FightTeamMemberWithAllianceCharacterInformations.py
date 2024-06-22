from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamMemberCharacterInformations import (
    FightTeamMemberCharacterInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicAllianceInformations import (
        BasicAllianceInformations,
    )


class FightTeamMemberWithAllianceCharacterInformations(FightTeamMemberCharacterInformations):
    allianceInfos: "BasicAllianceInformations"

    def init(self, allianceInfos_: "BasicAllianceInformations", name_: str, level_: int, id_: int):
        self.allianceInfos = allianceInfos_

        super().init(name_, level_, id_)
