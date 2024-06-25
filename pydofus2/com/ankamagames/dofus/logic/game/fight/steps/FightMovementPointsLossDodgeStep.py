from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.abstract.AbstractDodgePointLossStep import (
    AbstractDodgePointLossStep,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep


class FightMovementPointsLossDodgeStep(AbstractDodgePointLossStep, IFightStep):
    def __init__(self, fighterId: float, amount: int):
        super().__init__(fighterId, amount)

    @property
    def stepType(self) -> str:
        return "movementPointsLossDodge"

    def start(self) -> None:
        self.executeCallbacks()
