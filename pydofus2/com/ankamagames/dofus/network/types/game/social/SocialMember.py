from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalInformations import \
    CharacterMinimalInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import \
        PlayerStatus


class SocialMember(CharacterMinimalInformations):
    breed: int
    sex: bool
    connected: int
    hoursSinceLastConnection: int
    accountId: int
    status: "PlayerStatus"
    rankId: int
    enrollmentDate: int

    def init(
        self,
        breed_: int,
        sex_: bool,
        connected_: int,
        hoursSinceLastConnection_: int,
        accountId_: int,
        status_: "PlayerStatus",
        rankId_: int,
        enrollmentDate_: int,
        level_: int,
        name_: str,
        id_: int,
    ):
        self.breed = breed_
        self.sex = sex_
        self.connected = connected_
        self.hoursSinceLastConnection = hoursSinceLastConnection_
        self.accountId = accountId_
        self.status = status_
        self.rankId = rankId_
        self.enrollmentDate = enrollmentDate_

        super().init(level_, name_, id_)
