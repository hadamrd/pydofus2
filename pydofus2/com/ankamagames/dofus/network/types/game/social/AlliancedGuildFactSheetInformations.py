from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
    GuildInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicNamedAllianceInformations import \
        BasicNamedAllianceInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import \
        SocialEmblem


class AlliancedGuildFactSheetInformations(GuildInformations):
    allianceInfos: "BasicNamedAllianceInformations"

    def init(
        self,
        allianceInfos_: "BasicNamedAllianceInformations",
        guildEmblem_: "SocialEmblem",
        guildId_: int,
        guildName_: str,
        guildLevel_: int,
    ):
        self.allianceInfos = allianceInfos_

        super().init(guildEmblem_, guildId_, guildName_, guildLevel_)
