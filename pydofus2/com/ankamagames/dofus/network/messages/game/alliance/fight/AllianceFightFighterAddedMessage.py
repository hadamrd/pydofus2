from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalPlusLookInformations import \
        CharacterMinimalPlusLookInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.social.fight.SocialFightInfo import \
        SocialFightInfo
    

class AllianceFightFighterAddedMessage(NetworkMessage):
    allianceFightInfo: 'SocialFightInfo'
    fighter: 'CharacterMinimalPlusLookInformations'
    team: int
    def init(self, allianceFightInfo_: 'SocialFightInfo', fighter_: 'CharacterMinimalPlusLookInformations', team_: int):
        self.allianceFightInfo = allianceFightInfo_
        self.fighter = fighter_
        self.team = team_
        
        super().__init__()
    