from pydofus2.com.ankamagames.dofus.datacenter.effects.Effect import Effect
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceDice import EffectInstanceDice
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import BasicBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastSequenceContext import SpellCastSequenceContext
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTriggeredEffect import FightTriggeredEffect


class TriggeredBuff(BasicBuff):

    delay: int

    triggerCount: int

    def __init__(
        self,
        effect: FightTriggeredEffect = None,
        castingSpell: SpellCastSequenceContext = None,
        actionId: int = 0,
    ):
        if effect:
            super().__init__(
                effect,
                castingSpell,
                actionId,
                effect.param1,
                effect.param2,
                effect.param3,
            )
            self.initParam(effect.param1, effect.param2, effect.param3)
            self.delay = effect.delay
            self._effect.delay = self.delay
            self.triggerCount = 0

    @property
    def param1(self):
        return self._effect.parameter0

    @param1.setter
    def param1(self, value: int):
        self._effect.parameter0 = value

    @property
    def param2(self):
        return self._effect.parameter1

    @param2.setter
    def param2(self, value: int):
        self._effect.parameter1 = value

    @property
    def param3(self):
        return self._effect.parameter2

    @param3.setter
    def param3(self, value) -> None:
        self._effect.parameter2 = value

    def initParam(self, param1: int, param2: int, param3: int) -> None:
        min: int = 0
        max: int = 0
        super().initParam(param1, param2, param3)
        e: Effect = Effect.getEffectById(self.actionId)
        if e and e.forceMinMax and isinstance(self._effect, EffectInstanceDice):
            min = param3 + param1
            max = param1 * param2 + param3
            if min == max:
                self.param1 = min
                self.param3 = 0
                self.param2 = 0
            elif min > max:
                self.param1 = max
                self.param2 = min
                self.param3 = 0
            else:
                self.param1 = min
                self.param2 = max
                self.param3 = 0

    def clone(self, id: int = 0) -> BasicBuff:
        tb: TriggeredBuff = TriggeredBuff()
        tb.id = self.uid
        tb.uid = self.uid
        tb.dataUid = self.dataUid
        tb.actionId = self.actionId
        tb.targetId = self.targetId
        tb.castingSpell = self.castingSpell
        tb.duration = self.duration
        tb.dispelable = self.dispelable
        tb.source = self.source
        tb.aliveSource = self.aliveSource
        tb.sourceJustReaffected = self.sourceJustReaffected
        tb.parentBoostUid = self.parentBoostUid
        tb.initParam(self.param1, self.param2, self.param3)
        tb.delay = self.delay
        tb._effect.delay = self.delay
        return tb

    @property
    def active(self) -> bool:
        return self.delay > 0 or super().active

    @property
    def trigger(self) -> bool:
        return True

    def incrementDuration(self, delta: int, dispellEffect: bool = False) -> bool:
        if self.delay > 0 and not dispellEffect:
            if self.delay + delta >= 0:
                self.delay -= 1
                self.effect.delay -= 1
            else:
                delta += self.delay
                self.delay = 0
                self.effect.delay = 0
        if delta != 0:
            return super().incrementDuration(delta, dispellEffect)
        return True

    @property
    def unusableNextTurn(self) -> bool:
        return self.delay <= 1 and self.getUnuableNextTurn()
