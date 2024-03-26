from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.guild.application.GuildPlayerApplicationAbstractMessage import \
    GuildPlayerApplicationAbstractMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
        GuildInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.social.application.SocialApplicationInformation import \
        SocialApplicationInformation


class GuildPlayerApplicationInformationMessage(GuildPlayerApplicationAbstractMessage):
    guildInformation: "GuildInformations"
    apply: "SocialApplicationInformation"

    def init(self, guildInformation_: "GuildInformations", apply_: "SocialApplicationInformation"):
        self.guildInformation = guildInformation_
        self.apply = apply_

        super().init()
