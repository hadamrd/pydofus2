from pydofus2.com.ankamagames.dofus.logic.game.common.misc.ISpellCastProvider import \
    ISpellCastProvider
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.CastingSpell import \
    CastingSpell
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import \
    ISequencable


class SpellScriptBuffer(ISpellCastProvider):

    _steps: list[ISequencable]

    _castingSpell: CastingSpell

    def __init__(self, __castingSpell: CastingSpell):
        self._steps = list[ISequencable]()
        super().__init__()
        self._castingSpell = __castingSpell

    @property
    def castingSpell(self) -> CastingSpell:
        return self._castingSpell

    @property
    def stepsBuffer(self) -> list[ISequencable]:
        return self._steps
