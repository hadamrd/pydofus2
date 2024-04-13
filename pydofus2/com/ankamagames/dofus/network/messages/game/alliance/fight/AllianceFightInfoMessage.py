from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.fight.SocialFight import SocialFight


class AllianceFightInfoMessage(NetworkMessage):
    allianceFights: list["SocialFight"]

    def init(self, allianceFights_: list["SocialFight"]):
        self.allianceFights = allianceFights_

        super().__init__()
