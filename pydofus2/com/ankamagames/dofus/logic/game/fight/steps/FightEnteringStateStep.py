from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import BasicBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StateBuff import StateBuff
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightEnteringStateStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _stateId: int

    _durationString: str

    _buff: StateBuff

    def __init__(self, fighterId: float, stateId: int, durationString: str, buff: BasicBuff):
        super().__init__()
        self._fighterId = fighterId
        self._stateId = stateId
        self._durationString = durationString
        self._buff = buff

    @property
    def stepType(self) -> str:
        return "enteringState"

    def start(self) -> None:
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
