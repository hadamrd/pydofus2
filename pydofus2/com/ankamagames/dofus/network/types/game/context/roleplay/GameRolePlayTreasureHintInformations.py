from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import \
    GameRolePlayActorInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import \
        EntityDispositionInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook
    

class GameRolePlayTreasureHintInformations(GameRolePlayActorInformations):
    npcId: int
    def init(self, npcId_: int, look_: 'EntityLook', contextualId_: int, disposition_: 'EntityDispositionInformations'):
        self.npcId = npcId_
        
        super().init(look_, contextualId_, disposition_)
    