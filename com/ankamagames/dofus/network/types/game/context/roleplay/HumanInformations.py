from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from com.ankamagames.dofus.network.types.game.character.restriction.ActorRestrictionsInformations import ActorRestrictionsInformations
    from com.ankamagames.dofus.network.types.game.context.roleplay.HumanOption import HumanOption
    


class HumanInformations(NetworkMessage):
    restrictions:'ActorRestrictionsInformations'
    sex:bool
    options:list['HumanOption']
    

    def init(self, restrictions:'ActorRestrictionsInformations', sex:bool, options:list['HumanOption']):
        self.restrictions = restrictions
        self.sex = sex
        self.options = options
        
        super().__init__()
    
    