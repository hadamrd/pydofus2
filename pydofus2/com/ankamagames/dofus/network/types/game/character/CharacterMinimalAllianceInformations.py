from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalPlusLookInformations import \
    CharacterMinimalPlusLookInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicNamedAllianceInformations import \
        BasicNamedAllianceInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook
    

class CharacterMinimalAllianceInformations(CharacterMinimalPlusLookInformations):
    alliance: 'BasicNamedAllianceInformations'
    def init(self, alliance_: 'BasicNamedAllianceInformations', entityLook_: 'EntityLook', breed_: int, level_: int, name_: str, id_: int):
        self.alliance = alliance_
        
        super().init(entityLook_, breed_, level_, name_, id_)
    