from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.GuildMemberInfo import \
        GuildMemberInfo


class GuildInformationsMembersMessage(NetworkMessage):
    members: list["GuildMemberInfo"]

    def init(self, members_: list["GuildMemberInfo"]):
        self.members = members_

        super().__init__()
