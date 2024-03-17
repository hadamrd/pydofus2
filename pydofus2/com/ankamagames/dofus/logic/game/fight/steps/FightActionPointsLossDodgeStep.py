from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.abstract.AbstractDodgePointLossStep import \
    AbstractDodgePointLossStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep


class FightActionPointsLossDodgeStep(AbstractDodgePointLossStep, IFightStep):
    def __init__(self, fighterId: float, amount: int):
        super().__init__(fighterId, amount)

    @property
    def stepType(self) -> str:
        return "actionPointsLossDodge"

    def start(self) -> None:
        self.executeCallbacks()
