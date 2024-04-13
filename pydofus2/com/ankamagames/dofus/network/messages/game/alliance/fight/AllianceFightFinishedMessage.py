from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.fight.SocialFightInfo import SocialFightInfo


class AllianceFightFinishedMessage(NetworkMessage):
    allianceFightInfo: "SocialFightInfo"

    def init(self, allianceFightInfo_: "SocialFightInfo"):
        self.allianceFightInfo = allianceFightInfo_

        super().__init__()
