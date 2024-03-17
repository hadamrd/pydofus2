from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import \
    BasicBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.CastingSpell import \
    CastingSpell
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporarySpellBoostEffect import \
    FightTemporarySpellBoostEffect


class SpellBuff(BasicBuff):
    spellId: int

    delta: int

    modifType: int

    def __init__(
        self,
        effect: FightTemporarySpellBoostEffect = None,
        castingSpell: CastingSpell = None,
        actionId: int = 0,
    ):
        if effect:
            super().__init__(
                effect,
                castingSpell,
                actionId,
                effect.boostedSpellId,
                None,
                effect.delta,
            )
            self.spellId = effect.boostedSpellId
            self.delta = effect.delta

    @property
    def type(self) -> str:
        return "SpellBuff"

    def clone(self, id: int = 0) -> BasicBuff:
        sb: SpellBuff = SpellBuff()
        sb.spellId = self.spellId
        sb.delta = self.delta
        sb.modifType = self.modifType
        sb.id = self.uid
        sb.uid = self.uid
        sb.dataUid = self.dataUid
        sb.actionId = self.actionId
        sb.targetId = self.targetId
        sb.castingSpell = self.castingSpell
        sb.duration = self.duration
        sb.dispelable = self.dispelable
        sb.source = self.source
        sb.aliveSource = self.aliveSource
        sb.sourceJustReaffected = self.sourceJustReaffected
        sb.parentBoostUid = self.parentBoostUid
        sb.initParam(self.param1, self.param2, self.param3)
        return sb
