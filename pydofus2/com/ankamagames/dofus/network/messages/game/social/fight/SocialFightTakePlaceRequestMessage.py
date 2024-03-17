from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.fight.SocialFightInfo import \
        SocialFightInfo
    

class SocialFightTakePlaceRequestMessage(NetworkMessage):
    socialFightInfo: 'SocialFightInfo'
    replacedCharacterId: int
    def init(self, socialFightInfo_: 'SocialFightInfo', replacedCharacterId_: int):
        self.socialFightInfo = socialFightInfo_
        self.replacedCharacterId = replacedCharacterId_
        
        super().__init__()
    