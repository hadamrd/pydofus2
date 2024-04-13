from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporaryBoostEffect import (
    FightTemporaryBoostEffect,
)


class FightDetailedTemporaryBoostEffect(FightTemporaryBoostEffect):
    param1: int
    param2: int
    param3: int

    def init(
        self,
        param1_: int,
        param2_: int,
        param3_: int,
        delta_: int,
        uid_: int,
        targetId_: int,
        turnDuration_: int,
        dispelable_: int,
        spellId_: int,
        effectId_: int,
        parentBoostUid_: int,
    ):
        self.param1 = param1_
        self.param2 = param2_
        self.param3 = param3_

        super().init(delta_, uid_, targetId_, turnDuration_, dispelable_, spellId_, effectId_, parentBoostUid_)
