from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
    GuildInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import \
        SocialEmblem


class GuildInAllianceInformations(GuildInformations):
    nbMembers: int
    joinDate: int

    def init(
        self,
        nbMembers_: int,
        joinDate_: int,
        guildEmblem_: "SocialEmblem",
        guildId_: int,
        guildName_: str,
        guildLevel_: int,
    ):
        self.nbMembers = nbMembers_
        self.joinDate = joinDate_

        super().init(guildEmblem_, guildId_, guildName_, guildLevel_)
