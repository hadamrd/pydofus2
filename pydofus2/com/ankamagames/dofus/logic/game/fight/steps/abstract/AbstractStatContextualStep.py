from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class AbstractStatContextualStep(AbstractSequencable):

    _color: int

    _value: str

    _targetId: float

    _blocking: bool

    _virtual: bool

    _gameContext: int

    def __init__(
        self,
        color: int,
        value: str,
        targetId: float,
        gameContext: int,
        blocking: bool = True,
    ):
        super().__init__()
        self._color = color
        self._value = value
        self._targetId = targetId
        self._gameContext = gameContext
        self._blocking = blocking

    def start(self) -> None:
        self.executeCallbacks()

    @property
    def target(self) -> IEntity:
        return DofusEntities().getEntity(self._targetId)

    @property
    def targets(self) -> list[float]:
        return [self._targetId]
