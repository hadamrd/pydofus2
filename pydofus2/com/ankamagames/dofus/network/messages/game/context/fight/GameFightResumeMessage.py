from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightSpectateMessage import (
    GameFightSpectateMessage,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.action.fight.FightDispellableEffectExtendedInformations import (
        FightDispellableEffectExtendedInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.GameActionMark import GameActionMark
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightEffectTriggerCount import (
        GameFightEffectTriggerCount,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightSpellCooldown import (
        GameFightSpellCooldown,
    )


class GameFightResumeMessage(GameFightSpectateMessage):
    spellCooldowns: list["GameFightSpellCooldown"]
    summonCount: int
    bombCount: int

    def init(
        self,
        spellCooldowns_: list["GameFightSpellCooldown"],
        summonCount_: int,
        bombCount_: int,
        effects_: list["FightDispellableEffectExtendedInformations"],
        marks_: list["GameActionMark"],
        gameTurn_: int,
        fightStart_: int,
        fxTriggerCounts_: list["GameFightEffectTriggerCount"],
    ):
        self.spellCooldowns = spellCooldowns_
        self.summonCount = summonCount_
        self.bombCount = bombCount_

        super().init(effects_, marks_, gameTurn_, fightStart_, fxTriggerCounts_)
