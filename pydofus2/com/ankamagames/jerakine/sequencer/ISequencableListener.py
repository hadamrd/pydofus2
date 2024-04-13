from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import ISequencable


class ISequencableListener:
    def stepFinished(self, param1: ISequencable) -> None:
        raise NotImplementedError("Not implemented yet")
