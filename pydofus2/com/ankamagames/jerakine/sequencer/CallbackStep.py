from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable
from pydofus2.com.ankamagames.jerakine.types.Callback import Callback


class CallbackStep(AbstractSequencable):

    _callback: Callback

    def __init__(self, callback: Callback):
        super().__init__()
        self._callback = callback

    def start(self) -> None:
        self._callback.exec()
        self.executeCallbacks()
