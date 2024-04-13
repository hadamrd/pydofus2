from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.action.fight.FightDispellableEffectExtendedInformations import (
        FightDispellableEffectExtendedInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.GameActionMark import GameActionMark
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightEffectTriggerCount import (
        GameFightEffectTriggerCount,
    )


class GameFightSpectateMessage(NetworkMessage):
    effects: list["FightDispellableEffectExtendedInformations"]
    marks: list["GameActionMark"]
    gameTurn: int
    fightStart: int
    fxTriggerCounts: list["GameFightEffectTriggerCount"]

    def init(
        self,
        effects_: list["FightDispellableEffectExtendedInformations"],
        marks_: list["GameActionMark"],
        gameTurn_: int,
        fightStart_: int,
        fxTriggerCounts_: list["GameFightEffectTriggerCount"],
    ):
        self.effects = effects_
        self.marks = marks_
        self.gameTurn = gameTurn_
        self.fightStart = fightStart_
        self.fxTriggerCounts = fxTriggerCounts_

        super().__init__()
