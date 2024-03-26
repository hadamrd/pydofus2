from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.fight.SocialFightInfo import \
        SocialFightInfo


class AllianceFightFighterRemovedMessage(NetworkMessage):
    allianceFightInfo: "SocialFightInfo"
    fighterId: int

    def init(self, allianceFightInfo_: "SocialFightInfo", fighterId_: int):
        self.allianceFightInfo = allianceFightInfo_
        self.fighterId = fighterId_

        super().__init__()
