from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayGroupMonsterInformations import \
    GameRolePlayGroupMonsterInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import \
        EntityDispositionInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GroupMonsterStaticInformations import \
        GroupMonsterStaticInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook
    

class GameRolePlayGroupMonsterWaveInformations(GameRolePlayGroupMonsterInformations):
    nbWaves: int
    alternatives: list['GroupMonsterStaticInformations']
    def init(self, nbWaves_: int, alternatives_: list['GroupMonsterStaticInformations'], staticInfos_: 'GroupMonsterStaticInformations', lootShare_: int, alignmentSide_: int, hasHardcoreDrop_: bool, look_: 'EntityLook', contextualId_: int, disposition_: 'EntityDispositionInformations'):
        self.nbWaves = nbWaves_
        self.alternatives = alternatives_
        
        super().init(staticInfos_, lootShare_, alignmentSide_, hasHardcoreDrop_, look_, contextualId_, disposition_)
    