from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightTeamMemberInformations import (
    FightTeamMemberInformations,
)


class FightTeamMemberTaxCollectorInformations(FightTeamMemberInformations):
    firstNameId: int
    lastNameId: int
    groupId: int
    uid: int

    def init(self, firstNameId_: int, lastNameId_: int, groupId_: int, uid_: int, id_: int):
        self.firstNameId = firstNameId_
        self.lastNameId = lastNameId_
        self.groupId = groupId_
        self.uid = uid_

        super().init(id_)
