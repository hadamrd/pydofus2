import sys

from pydofus2.com.ankamagames.berilia.managers.EventsHandler import \
    EventsHandler
from pydofus2.com.ankamagames.jerakine.events.SequencerEvent import \
    SequencerEvent
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable
from pydofus2.com.ankamagames.jerakine.sequencer.IPausableSequencable import \
    IPausableSequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import \
    ISequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencer import ISequencer
from pydofus2.com.ankamagames.jerakine.sequencer.ISubSequenceSequencable import \
    ISubSequenceSequencable


class SerialSequencer(ISequencer, EventsHandler):

    DEFAULT_SEQUENCER_NAME: str = "SerialSequencerDefault"

    _defaultStepTimeout: int = -2147483648

    def __init__(self, type: str = "SerialSequencerDefault"):
        self._steps = list[ISequencable]()
        self._activeSubSequenceCount = 0
        self._currentStep: ISequencable = None
        self._lastStep: ISequencable = None
        self._paused: bool = None
        self._running: bool = False
        self._type: str = type
        super().__init__()

    @property
    def currentStep(self) -> ISequencable:
        return self._currentStep

    @property
    def lastStep(self) -> ISequencable:
        return self._lastStep

    @property
    def length(self) -> int:
        return len(self._steps)

    @property
    def running(self) -> bool:
        return self._running

    @property
    def steps(self) -> list:
        return self._steps

    def pause(self) -> None:
        self._paused = True
        if isinstance(self._currentStep, IPausableSequencable):
            self._currentStep.pause()

    def resume(self) -> None:
        self._paused = False
        if isinstance(self._currentStep, IPausableSequencable):
            self._currentStep.start()

    def add(self, item: ISequencable) -> None:
        if item:
            self.addStep(item)

    def addStep(self, item: ISequencable) -> None:
        self._steps.append(item)

    def start(self) -> None:
        if not self._running:
            self._running = len(self._steps) != 0
            if self._running:
                while self._steps and self._running:
                    self.execute()
                    if (
                        self._currentStep
                        and isinstance(self._currentStep, AbstractSequencable)
                        and not self._currentStep.finished
                    ):
                        self._running = False
                if not self._running:
                    self._running = False
                    self.send(SequencerEvent.SEQUENCE_END, SequencerEvent(self))

    def clear(self) -> None:
        self._lastStep = None
        if self._currentStep:
            self._currentStep.clear()
            self._currentStep = None
        for step in self._steps:
            if step:
                step.clear()
        self._steps.clear()
        self._running = False

    def __str__(self) -> str:
        res: str = ""
        for step in self._steps:
            res += str(step) + "\n"
        return res

    def execute(self) -> None:
        self._lastStep = self._currentStep
        self._currentStep = self._steps.pop(0)
        if not self._currentStep:
            return
        self._currentStep.addListener(self)
        try:
            if isinstance(self._currentStep, ISubSequenceSequencable):
                self._activeSubSequenceCount += 1
                self._currentStep.on(SequencerEvent.SEQUENCE_END, self.onSubSequenceEnd)
            if self._defaultStepTimeout != -sys.maxsize - 1 and self._currentStep.hasDefaultTimeout:
                self._currentStep.timeout = self._defaultStepTimeout
            self.send(
                SequencerEvent.SEQUENCE_STEP_START,
                SequencerEvent(self, self._currentStep),
            )
            self._currentStep.start()
        except Exception as e:
            if isinstance(self._currentStep, ISubSequenceSequencable):
                self._activeSubSequenceCount -= 1
                self._currentStep.remove_listener(SequencerEvent.SEQUENCE_END, self.onSubSequenceEnd)
            Logger().error(f"Exception on step {self._currentStep}", exc_info=True)
            if isinstance(self._currentStep, AbstractSequencable):
                self._currentStep.finished = True
            self.stepFinished(self._currentStep)

    def stepFinished(self, step: ISequencable) -> None:
        step.removeListener(self)
        if self._running:
            self.send(
                SequencerEvent.SEQUENCE_STEP_FINISH,
                SequencerEvent(self, self._currentStep),
            )
            self._running = len(self._steps) != 0
            if not self._running:
                if self._activeSubSequenceCount < 1:
                    self.send(SequencerEvent.SEQUENCE_END, SequencerEvent(self))
                else:
                    self._running = True
        else:
            self.send(SequencerEvent.SEQUENCE_STEP_FINISH, SequencerEvent(self, self._currentStep))
            self.start()

    def onSubSequenceEnd(self, evt_id, e: SequencerEvent = None) -> None:
        self._activeSubSequenceCount -= 1
        if not self._activeSubSequenceCount and len(self._steps) == 0:
            self._running = False
            self.send(SequencerEvent.SEQUENCE_END, SequencerEvent(self))
