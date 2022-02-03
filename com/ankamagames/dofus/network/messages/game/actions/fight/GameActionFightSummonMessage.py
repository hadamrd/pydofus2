from com.ankamagames.dofus.network.messages.game.actions.AbstractGameActionMessage import AbstractGameActionMessage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import GameFightFighterInformations
    


class GameActionFightSummonMessage(AbstractGameActionMessage):
    summons:list['GameFightFighterInformations']
    

    def init(self, summons:list['GameFightFighterInformations'], actionId:int, sourceId:int):
        self.summons = summons
        
        super().__init__(actionId, sourceId)
    
    