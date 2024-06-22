from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import SocialEmblem


class GuildModificationEmblemValidMessage(NetworkMessage):
    guildEmblem: "SocialEmblem"

    def init(self, guildEmblem_: "SocialEmblem"):
        self.guildEmblem = guildEmblem_

        super().__init__()
