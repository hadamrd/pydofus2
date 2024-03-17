from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightPhase import \
        FightPhase
    from pydofus2.com.ankamagames.dofus.network.types.game.social.fight.SocialFightInfo import \
        SocialFightInfo
    

class AllianceFightStartedMessage(NetworkMessage):
    allianceFightInfo: 'SocialFightInfo'
    phase: 'FightPhase'
    def init(self, allianceFightInfo_: 'SocialFightInfo', phase_: 'FightPhase'):
        self.allianceFightInfo = allianceFightInfo_
        self.phase = phase_
        
        super().__init__()
    