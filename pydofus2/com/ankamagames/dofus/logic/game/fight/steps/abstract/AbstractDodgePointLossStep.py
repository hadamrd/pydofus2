from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class AbstractDodgePointLossStep(AbstractSequencable):

    _fighterId: float

    _amount: int

    def __init__(self, fighterId: float, amount: int):
        super().__init__()
        self._fighterId = fighterId
        self._amount = amount

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
