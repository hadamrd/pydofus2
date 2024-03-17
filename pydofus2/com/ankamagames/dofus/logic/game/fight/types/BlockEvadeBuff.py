from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.types.CastingSpell import CastingSpell
    from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporaryBoostEffect import (
        FightTemporaryBoostEffect,
    )

from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StatBuff import \
    StatBuff


class BlockEvadeBuff(StatBuff):
    def __init__(
        self,
        effect: "FightTemporaryBoostEffect" = None,
        castingSpell: "CastingSpell" = None,
        actionId: int = 0,
    ):
        super().__init__(effect, castingSpell, actionId)

    def onApplied(self) -> None:
        super().onApplied()

    def onRemoved(self) -> None:
        super().onRemoved()
