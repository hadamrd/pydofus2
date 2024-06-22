from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicGuildInformations import (
    BasicGuildInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import SocialEmblem


class GuildInformations(BasicGuildInformations):
    guildEmblem: "SocialEmblem"

    def init(self, guildEmblem_: "SocialEmblem", guildId_: int, guildName_: str, guildLevel_: int):
        self.guildEmblem = guildEmblem_

        super().init(guildId_, guildName_, guildLevel_)
