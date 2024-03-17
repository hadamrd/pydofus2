from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
    GameFightFighterInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import \
        EntityDispositionInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameContextBasicSpawnInformation import \
        GameContextBasicSpawnInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacteristics import \
        GameFightCharacteristics
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook
    

class GameFightEntityInformation(GameFightFighterInformations):
    entityModelId: int
    level: int
    masterId: int
    def init(self, entityModelId_: int, level_: int, masterId_: int, spawnInfo_: 'GameContextBasicSpawnInformation', wave_: int, stats_: 'GameFightCharacteristics', previousPositions_: list[int], look_: 'EntityLook', contextualId_: int, disposition_: 'EntityDispositionInformations'):
        self.entityModelId = entityModelId_
        self.level = level_
        self.masterId = masterId_
        
        super().init(spawnInfo_, wave_, stats_, previousPositions_, look_, contextualId_, disposition_)
    