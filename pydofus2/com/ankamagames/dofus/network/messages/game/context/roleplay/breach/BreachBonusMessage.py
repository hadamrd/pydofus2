from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectInteger import \
        ObjectEffectInteger
    

class BreachBonusMessage(NetworkMessage):
    bonus: 'ObjectEffectInteger'
    def init(self, bonus_: 'ObjectEffectInteger'):
        self.bonus = bonus_
        
        super().__init__()
    