from typing import List, Optional

from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastSequenceContext import SpellCastSequenceContext
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import ISequencable

class SpellCastSequence:

    def __init__(self, context: 'SpellCastSequenceContext', steps: Optional[List['ISequencable']] = None):
        self._context = context
        self._steps = steps if steps is not None else []

    @property
    def context(self) -> 'SpellCastSequenceContext':
        return self._context

    @context.setter
    def context(self, context: 'SpellCastSequenceContext') -> None:
        self._context = context

    @property
    def steps(self) -> List['ISequencable']:
        return self._steps

    @steps.setter
    def steps(self, steps: List['ISequencable']) -> None:
        self._steps = steps
