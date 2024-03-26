from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamInformations import \
    FightTeamInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamMemberInformations import \
        FightTeamMemberInformations


class FightAllianceTeamInformations(FightTeamInformations):
    relation: int

    def init(
        self,
        relation_: int,
        teamMembers_: list["FightTeamMemberInformations"],
        teamId_: int,
        leaderId_: int,
        teamSide_: int,
        teamTypeId_: int,
        nbWaves_: int,
    ):
        self.relation = relation_

        super().init(teamMembers_, teamId_, leaderId_, teamSide_, teamTypeId_, nbWaves_)
