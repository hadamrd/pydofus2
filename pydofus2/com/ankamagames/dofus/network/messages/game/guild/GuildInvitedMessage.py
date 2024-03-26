from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
        GuildInformations


class GuildInvitedMessage(NetworkMessage):
    recruterName: str
    guildInfo: "GuildInformations"

    def init(self, recruterName_: str, guildInfo_: "GuildInformations"):
        self.recruterName = recruterName_
        self.guildInfo = guildInfo_

        super().__init__()
