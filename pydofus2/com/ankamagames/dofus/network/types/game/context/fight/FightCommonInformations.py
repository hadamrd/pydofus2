from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightOptionsInformations import \
        FightOptionsInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamInformations import \
        FightTeamInformations
    

class FightCommonInformations(NetworkMessage):
    fightId: int
    fightType: int
    fightTeams: list['FightTeamInformations']
    fightTeamsPositions: list[int]
    fightTeamsOptions: list['FightOptionsInformations']
    def init(self, fightId_: int, fightType_: int, fightTeams_: list['FightTeamInformations'], fightTeamsPositions_: list[int], fightTeamsOptions_: list['FightOptionsInformations']):
        self.fightId = fightId_
        self.fightType = fightType_
        self.fightTeams = fightTeams_
        self.fightTeamsPositions = fightTeamsPositions_
        self.fightTeamsOptions = fightTeamsOptions_
        
        super().__init__()
    