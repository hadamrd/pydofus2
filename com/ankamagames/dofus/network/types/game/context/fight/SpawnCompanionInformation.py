from com.ankamagames.dofus.network.types.game.context.fight.SpawnInformation import SpawnInformation


class SpawnCompanionInformation(SpawnInformation):
    modelId:int
    level:int
    summonerId:int
    ownerId:int
    

    def init(self, modelId:int, level:int, summonerId:int, ownerId:int):
        self.modelId = modelId
        self.level = level
        self.summonerId = summonerId
        self.ownerId = ownerId
        
        super().__init__()
    
    