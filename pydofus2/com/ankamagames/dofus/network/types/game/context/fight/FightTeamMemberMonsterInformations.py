from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamMemberInformations import (
    FightTeamMemberInformations,
)


class FightTeamMemberMonsterInformations(FightTeamMemberInformations):
    monsterId: int
    grade: int

    def init(self, monsterId_: int, grade_: int, id_: int):
        self.monsterId = monsterId_
        self.grade = grade_

        super().init(id_)
