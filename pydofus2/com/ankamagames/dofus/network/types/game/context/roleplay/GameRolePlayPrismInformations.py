from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import \
    GameRolePlayActorInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import \
        EntityDispositionInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook
    from pydofus2.com.ankamagames.dofus.network.types.game.prism.PrismInformation import \
        PrismInformation
    

class GameRolePlayPrismInformations(GameRolePlayActorInformations):
    prism: 'PrismInformation'
    def init(self, prism_: 'PrismInformation', look_: 'EntityLook', contextualId_: int, disposition_: 'EntityDispositionInformations'):
        self.prism = prism_
        
        super().init(look_, contextualId_, disposition_)
    