from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.fight.SocialFightInfo import SocialFightInfo


class SocialFightLeaveRequestMessage(NetworkMessage):
    socialFightInfo: "SocialFightInfo"

    def init(self, socialFightInfo_: "SocialFightInfo"):
        self.socialFightInfo = socialFightInfo_

        super().__init__()
