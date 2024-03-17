from pydofus2.com.ankamagames.dofus.logic.game.fight.types.CastingSpell import \
    CastingSpell
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import \
    ISequencable


class ISpellCastProvider:
    @property
    def castingSpell(self) -> CastingSpell:
        raise NotImplementedError()

    @property
    def stepsBuffer(self) -> list[ISequencable]:
        raise NotImplementedError()
