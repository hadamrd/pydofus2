from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencer import ISequencer
from pydofus2.com.ankamagames.jerakine.sequencer.ISubSequenceSequencable import \
    ISubSequenceSequencable
from pydofus2.com.ankamagames.jerakine.types.events.SequencerEvent import \
    SequencerEvent


class ParallelStartSequenceStep(AbstractSequencable, ISubSequenceSequencable):

    _aSequence: list[ISequencer]

    _waitAllSequenceEnd: bool

    _waitFirstEndSequence: bool

    _sequenceEndCount: int = 0

    def __init__(
        self,
        aSequence: list,
        waitAllSequenceEnd: bool = True,
        waitFirstEndSequence: bool = False,
    ):
        super().__init__()
        self._aSequence = aSequence
        self._waitAllSequenceEnd = waitAllSequenceEnd
        self._waitFirstEndSequence = waitFirstEndSequence

    def start(self) -> None:
        for i in range(len(self._aSequence)):
            self._aSequence[i].once(SequencerEvent.SEQUENCE_END, self.onSequenceEnd)
            # Logger().debug(f"ParallelStartSequenceStep start sequencer {i} that has {self._aSequence[i].steps} steps")
            self._aSequence[i].start()
        if not self._waitAllSequenceEnd and not self._waitFirstEndSequence:
            # Logger().debug("first executeCallbacks")
            self.executeCallbacks()

    @property
    def sequenceEndCount(self) -> int:
        return self._sequenceEndCount

    def onSequenceEnd(self, e_id, e: SequencerEvent=None) -> None:
        self._sequenceEndCount += 1
        if self._sequenceEndCount == len(self._aSequence):
            self.executeCallbacks()
            self.send(SequencerEvent.SEQUENCE_END, SequencerEvent(SequencerEvent.SEQUENCE_END))
        elif not self._waitAllSequenceEnd:
            if self._sequenceEndCount == 1:
                self.executeCallbacks()
