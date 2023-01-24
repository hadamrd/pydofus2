from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.types.Fight import Fight
from pydofus2.com.ankamagames.dofus.network.enums.FightOptionsEnum import FightOptionsEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import (
    GameContextActorInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightOptionsInformations import (
    FightOptionsInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamInformations import (
    FightTeamInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamMemberCharacterInformations import (
    FightTeamMemberCharacterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamMemberInformations import (
    FightTeamMemberInformations,
)
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class FightTeam(GameContextActorInformations):

    logger = Logger("Dofus2")

    fight: "Fight"

    teamType: int

    teamEntity: IEntity

    teamInfos: FightTeamInformations

    teamOptions: list

    def __init__(
        self,
        fight: "Fight",
        teamType: int,
        teamEntity: IEntity,
        teamInfos: FightTeamInformations,
        teamOptions: FightOptionsInformations,
    ):
        super().__init__()
        self.fight = fight
        self.teamType = teamType
        self.teamEntity = teamEntity
        self.teamInfos = teamInfos
        self.teamOptions = [False] * 4
        self.teamOptions[FightOptionsEnum.FIGHT_OPTION_ASK_FOR_HELP] = teamOptions.isAskingForHelp
        self.teamOptions[FightOptionsEnum.FIGHT_OPTION_SET_CLOSED] = teamOptions.isClosed
        self.teamOptions[FightOptionsEnum.FIGHT_OPTION_SET_SECRET] = teamOptions.isSecret
        self.teamOptions[FightOptionsEnum.FIGHT_OPTION_SET_TO_PARTY_ONLY] = teamOptions.isRestrictedToPartyOnly

    def hasGroupMember(self) -> bool:
        partyMember: PartyMemberWrapper = None
        fightTeamMember: FightTeamMemberInformations = None
        teamHasGroupMember: bool = False
        pmf: PartyManagementFrame = Kernel().worker.getFrame("PartyManagementFrame")
        partyMemberNames: list[str] = list[str]()
        for partyMember in pmf.partyMembers:
            partyMemberNames.append(partyMember.name)
        for fightTeamMember in self.teamInfos.teamMembers:
            if (
                fightTeamMember
                and isinstance(fightTeamMember, FightTeamMemberCharacterInformations)
                and FightTeamMemberCharacterInformations(fightTeamMember).name in partyMemberNames
            ):
                teamHasGroupMember = True
        return teamHasGroupMember

    def hasOptions(self) -> bool:
        opt = None
        hasOptions: bool = False
        for opt in self.teamOptions:
            if self.teamOptions.get(opt):
                hasOptions = True
        return hasOptions
