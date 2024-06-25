from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightRemoveSubEntityStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _category: int

    _slot: int

    def __init__(self, fighterId: float, category: int, slot: int):
        super().__init__()
        self._fighterId = fighterId
        self._category = category
        self._slot = slot

    @property
    def stepType(self) -> str:
        return "removeSubEntity"

    def start(self) -> None:
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
