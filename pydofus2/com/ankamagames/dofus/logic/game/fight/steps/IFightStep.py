from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import ISequencable


class IFightStep(ISequencable):
    @property
    def stepType(self) -> str:
        raise NotImplementedError()

    @property
    def castingSpellId(self) -> int:
        raise NotImplementedError()

    @castingSpellId.setter
    def castingSpellId(self, param1: int) -> None:
        raise NotImplementedError()

    @property
    def targets(self) -> list[float]:
        raise NotImplementedError()
