from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightSpellCastStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _cellId: int

    _sourceCellId: int

    _spellId: int

    _spellRank: int

    _critical: int

    _portalIds: list[int]

    _verboseCast: bool

    def __init__(
        self,
        fighterId: float,
        cellId: int,
        sourceCellId: int,
        spellId: int,
        spellRank: int,
        critical: int,
        verboseCast: bool,
    ):
        super().__init__()
        self._fighterId = fighterId
        self._cellId = cellId
        self._sourceCellId = sourceCellId
        self._spellId = spellId
        self._spellRank = spellRank
        self._critical = critical
        self._verboseCast = verboseCast

    @property
    def stepType(self) -> str:
        return "spellCast"

    def start(self) -> None:
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
