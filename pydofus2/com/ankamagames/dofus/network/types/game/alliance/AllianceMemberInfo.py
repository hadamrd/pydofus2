from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialMember import \
    SocialMember

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import \
        PlayerStatus


class AllianceMemberInfo(SocialMember):
    avaRoleId: int

    def init(
        self,
        avaRoleId_: int,
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
        self.avaRoleId = avaRoleId_

        super().init(
            breed_,
            sex_,
            connected_,
            hoursSinceLastConnection_,
            accountId_,
            status_,
            rankId_,
            enrollmentDate_,
            level_,
            name_,
            id_,
        )
