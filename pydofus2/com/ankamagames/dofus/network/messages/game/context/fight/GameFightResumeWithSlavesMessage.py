from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightResumeMessage import \
    GameFightResumeMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.action.fight.FightDispellableEffectExtendedInformations import \
        FightDispellableEffectExtendedInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.GameActionMark import \
        GameActionMark
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightEffectTriggerCount import \
        GameFightEffectTriggerCount
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightResumeSlaveInfo import \
        GameFightResumeSlaveInfo
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightSpellCooldown import \
        GameFightSpellCooldown
    

class GameFightResumeWithSlavesMessage(GameFightResumeMessage):
    slavesInfo: list['GameFightResumeSlaveInfo']
    def init(self, slavesInfo_: list['GameFightResumeSlaveInfo'], spellCooldowns_: list['GameFightSpellCooldown'], summonCount_: int, bombCount_: int, effects_: list['FightDispellableEffectExtendedInformations'], marks_: list['GameActionMark'], gameTurn_: int, fightStart_: int, fxTriggerCounts_: list['GameFightEffectTriggerCount']):
        self.slavesInfo = slavesInfo_
        
        super().init(spellCooldowns_, summonCount_, bombCount_, effects_, marks_, gameTurn_, fightStart_, fxTriggerCounts_)
    