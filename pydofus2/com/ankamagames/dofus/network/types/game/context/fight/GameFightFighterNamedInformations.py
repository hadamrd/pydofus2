from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
    GameFightFighterInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import \
        PlayerStatus
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import \
        EntityDispositionInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameContextBasicSpawnInformation import \
        GameContextBasicSpawnInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacteristics import \
        GameFightCharacteristics
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook
    

class GameFightFighterNamedInformations(GameFightFighterInformations):
    name: str
    status: 'PlayerStatus'
    leagueId: int
    ladderPosition: int
    hiddenInPrefight: bool
    def init(self, name_: str, status_: 'PlayerStatus', leagueId_: int, ladderPosition_: int, hiddenInPrefight_: bool, spawnInfo_: 'GameContextBasicSpawnInformation', wave_: int, stats_: 'GameFightCharacteristics', previousPositions_: list[int], look_: 'EntityLook', contextualId_: int, disposition_: 'EntityDispositionInformations'):
        self.name = name_
        self.status = status_
        self.leagueId = leagueId_
        self.ladderPosition = ladderPosition_
        self.hiddenInPrefight = hiddenInPrefight_
        
        super().init(spawnInfo_, wave_, stats_, previousPositions_, look_, contextualId_, disposition_)
    