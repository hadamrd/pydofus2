from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import BasicBuff
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightTemporaryBoostStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _statName: str

    _duration: int

    _durationText: str

    _visibleInLog: bool

    _buff: BasicBuff

    def __init__(
        self,
        fighterId: float,
        statName: str,
        duration: int,
        durationText: str,
        visible: bool = True,
        buff: BasicBuff = None,
    ):
        super().__init__()
        self._fighterId = fighterId
        self._statName = statName
        self._duration = duration
        self._durationText = durationText
        self._visibleInLog = visible
        self._buff = buff

    @property
    def stepType(self) -> str:
        return "temporaryBoost"

    def start(self) -> None:
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
