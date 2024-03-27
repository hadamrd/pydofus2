from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import ISequencable


class ISpellCastSequence:
    
    @property
    def context(self):
        pass
    
    @context.setter
    def context(self, context):
        pass
    
    @property
    def steps(self) -> list[ISequencable]:
        pass
    
    @steps.setter
    def steps(self, steps: list[ISequencable]):
        pass