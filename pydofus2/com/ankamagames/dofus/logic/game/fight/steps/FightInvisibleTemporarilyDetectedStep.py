from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightInvisibleTemporarilyDetectedStep(AbstractSequencable, IFightStep):

    def __init__(self, targetId, cellId: int):
        super().__init__()
        self._targetId = targetId
        self._cellId = cellId

    @property
    def stepType(self) -> str:
        return "invisibleTemporarilyDetected"

    def start(self) -> None:
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._targetId]
