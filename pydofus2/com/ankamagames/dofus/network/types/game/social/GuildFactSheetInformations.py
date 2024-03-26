from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
    GuildInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.recruitment.GuildRecruitmentInformation import \
        GuildRecruitmentInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import \
        SocialEmblem


class GuildFactSheetInformations(GuildInformations):
    leaderId: int
    nbMembers: int
    lastActivityDay: int
    recruitment: "GuildRecruitmentInformation"
    nbPendingApply: int

    def init(
        self,
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
        self.leaderId = leaderId_
        self.nbMembers = nbMembers_
        self.lastActivityDay = lastActivityDay_
        self.recruitment = recruitment_
        self.nbPendingApply = nbPendingApply_

        super().init(guildEmblem_, guildId_, guildName_, guildLevel_)
