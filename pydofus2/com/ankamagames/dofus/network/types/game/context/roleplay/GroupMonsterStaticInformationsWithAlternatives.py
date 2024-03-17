from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GroupMonsterStaticInformations import \
    GroupMonsterStaticInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AlternativeMonstersInGroupLightInformations import \
        AlternativeMonstersInGroupLightInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterInGroupInformations import \
        MonsterInGroupInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterInGroupLightInformations import \
        MonsterInGroupLightInformations
    

class GroupMonsterStaticInformationsWithAlternatives(GroupMonsterStaticInformations):
    alternatives: list['AlternativeMonstersInGroupLightInformations']
    def init(self, alternatives_: list['AlternativeMonstersInGroupLightInformations'], mainCreatureLightInfos_: 'MonsterInGroupLightInformations', underlings_: list['MonsterInGroupInformations']):
        self.alternatives = alternatives_
        
        super().init(mainCreatureLightInfos_, underlings_)
    