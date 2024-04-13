from pydofus2.com.ankamagames.dofus.logic.game.roleplay.types.FightTeam import FightTeam


class Fight:
    fightId: int
    teams: list[FightTeam]

    def __init__(self, fightId: int, teams: list[FightTeam]):
        self.fightId = fightId
        self.teams = teams

    def getTeamByType(self, teamType: int) -> FightTeam:
        team: FightTeam = None
        for team in self.teams:
            if team.teamType == teamType:
                return team
        return None

    def getTeamById(self, teamId: int) -> FightTeam:
        for team in self.teams:
            if team.teamInfos.teamId == teamId:
                return team
        return None
