from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.application.SocialApplicationInformation import \
        SocialApplicationInformation
    

class GuildListApplicationModifiedMessage(NetworkMessage):
    apply: 'SocialApplicationInformation'
    state: int
    playerId: int
    def init(self, apply_: 'SocialApplicationInformation', state_: int, playerId_: int):
        self.apply = apply_
        self.state = state_
        self.playerId = playerId_
        
        super().__init__()
    