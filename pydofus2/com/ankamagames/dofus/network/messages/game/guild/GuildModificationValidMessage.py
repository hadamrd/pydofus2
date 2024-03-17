from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import \
        SocialEmblem
    

class GuildModificationValidMessage(NetworkMessage):
    guildName: str
    guildEmblem: 'SocialEmblem'
    def init(self, guildName_: str, guildEmblem_: 'SocialEmblem'):
        self.guildName = guildName_
        self.guildEmblem = guildEmblem_
        
        super().__init__()
    