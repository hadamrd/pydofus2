from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightBattleFrame import (
        FightBattleFrame,
    )
    from pydofus2.com.ankamagames.jerakine.sequencer.ISequencer import ISequencer
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightTurnListStep(AbstractSequencable, IFightStep):

    _throwSubSequence: "ISequencer"

    _newTurnsList: list[float]

    _newDeadTurnsList: list[float]

    _turnsList: list[float]

    _deadTurnsList: list[float]

    def __init__(self, turnsList: list[float], deadTurnsList: list[float]):
        super().__init__()
        self._turnsList = turnsList
        self._deadTurnsList = deadTurnsList

    @property
    def stepType(self) -> str:
        return "turnList"

    def start(self) -> None:
        fbf: "FightBattleFrame" = Kernel().worker.getFrame("FightBattleFrame")
        if fbf:
            fbf.fightersList = self._turnsList
            fbf.deadFightersList = self._deadTurnsList
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return self._turnsList
