from com.ankamagames.dofus.network.types.game.context.fight.GameFightAIInformations import GameFightAIInformations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from com.ankamagames.dofus.network.types.game.context.fight.GameContextBasicSpawnInformation import GameContextBasicSpawnInformation
    from com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacteristics import GameFightCharacteristics
    from com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook
    from com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import EntityDispositionInformations
    


class GameFightMonsterInformations(GameFightAIInformations):
    creatureGenericId:int
    creatureGrade:int
    creatureLevel:int
    

    def init(self, creatureGenericId:int, creatureGrade:int, creatureLevel:int, spawnInfo:'GameContextBasicSpawnInformation', wave:int, stats:'GameFightCharacteristics', previousPositions:list[int], look:'EntityLook', contextualId:int, disposition:'EntityDispositionInformations'):
        self.creatureGenericId = creatureGenericId
        self.creatureGrade = creatureGrade
        self.creatureLevel = creatureLevel
        
        super().__init__(spawnInfo, wave, stats, previousPositions, look, contextualId, disposition)
    
    