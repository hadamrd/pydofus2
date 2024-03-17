from pydofus2.com.ankamagames.jerakine.sequencer.IPausableSequencable import \
    IPausableSequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencableListener import \
    ISequencableListener


class AbstractSequencable(IPausableSequencable):

    DEFAULT_TIMEOUT: int = 2

    def __init__(self):
        self._stepListeners = set()
        self._castingSpellId: int = -1
        self._paused: bool = False
        self._finished: bool = False
        super().__init__()

    @property
    def paused(self) -> bool:
        return self._paused

    @property
    def finished(self) -> bool:
        return self._finished

    @finished.setter
    def finished(self, bool: bool) -> None:
        self._finished = bool

    def pause(self) -> None:

        self._paused = True

    def resume(self) -> None:
        self._paused = False

    def start(self) -> None:
        pass

    def addListener(self, listener: ISequencableListener) -> None:
        if not self._stepListeners:
            self._stepListeners = set()
        self._stepListeners.add(listener)

    def executeCallbacks(self) -> None:
        self._finished = True
        if self._stepListeners:
            for listener in self._stepListeners.copy():
                if listener:
                    listener.stepFinished(self)

    def removeListener(self, listener: ISequencableListener) -> None:
        if not self._stepListeners:
            return
        self._stepListeners.remove(listener)

    def __str__(self) -> str:
        return self.__class__.__name__

    def clear(self) -> None:
        self._stepListeners = None

    @property
    def castingSpellId(self) -> int:
        return self._castingSpellId

    @castingSpellId.setter
    def castingSpellId(self, val: int) -> None:
        self._castingSpellId = val
