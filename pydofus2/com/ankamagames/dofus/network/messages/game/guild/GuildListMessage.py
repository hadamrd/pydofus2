from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
        GuildInformations


class GuildListMessage(NetworkMessage):
    guilds: list["GuildInformations"]

    def init(self, guilds_: list["GuildInformations"]):
        self.guilds = guilds_

        super().__init__()
