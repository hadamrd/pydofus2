from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightStealingKamasStep(AbstractSequencable, IFightStep):

    _robberId: float

    _victimId: float

    _amount: float = 0

    def __init__(self, robberId: float, victimId: float, amount: float):
        super().__init__()
        self._robberId = robberId
        self._victimId = victimId
        self._amount = amount

    @property
    def stepType(self) -> str:
        return "stealingKamas"

    def start(self) -> None:
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._victimId]
