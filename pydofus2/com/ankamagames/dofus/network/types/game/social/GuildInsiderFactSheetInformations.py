from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.social.GuildFactSheetInformations import \
    GuildFactSheetInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.recruitment.GuildRecruitmentInformation import \
        GuildRecruitmentInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import \
        SocialEmblem


class GuildInsiderFactSheetInformations(GuildFactSheetInformations):
    leaderName: str

    def init(
        self,
        leaderName_: str,
        leaderId_: int,
        nbMembers_: int,
        lastActivityDay_: int,
        recruitment_: "GuildRecruitmentInformation",
        nbPendingApply_: int,
        guildEmblem_: "SocialEmblem",
        guildId_: int,
        guildName_: str,
        guildLevel_: int,
    ):
        self.leaderName = leaderName_

        super().init(
            leaderId_,
            nbMembers_,
            lastActivityDay_,
            recruitment_,
            nbPendingApply_,
            guildEmblem_,
            guildId_,
            guildName_,
            guildLevel_,
        )
