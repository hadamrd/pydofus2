from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterInGroupInformations import \
        MonsterInGroupInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.MonsterInGroupLightInformations import \
        MonsterInGroupLightInformations
    

class GroupMonsterStaticInformations(NetworkMessage):
    mainCreatureLightInfos: 'MonsterInGroupLightInformations'
    underlings: list['MonsterInGroupInformations']
    def init(self, mainCreatureLightInfos_: 'MonsterInGroupLightInformations', underlings_: list['MonsterInGroupInformations']):
        self.mainCreatureLightInfos = mainCreatureLightInfos_
        self.underlings = underlings_
        
        super().__init__()
    