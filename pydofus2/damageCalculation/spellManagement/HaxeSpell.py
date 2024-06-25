from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.damageCalculation.fighterManagement.HaxeSpellEffect import HaxeSpellEffect


class HaxeSpell:
    def __init__(
        self,
        param1: int,
        param2: list,
        param3: list,
        param4: int,
        param5: bool,
        param6: bool,
        param7: int,
        param8: int,
        param9: int,
        param10: bool,
        param11: bool,
        param12: bool,
        param13: int = -1,
    ):
        self.canBeReflected = True
        self.isRune = False
        self.isGlyph = False
        self.isTrap = False
        self.isWeapon = False
        self._effects = param2
        self._criticalEffects = param3
        self.id = param1
        self.minimaleRange = 1
        self.maximaleRange = 1
        self.level = param4
        self.canAlwaysTriggerSpells = param5
        self.isWeapon = param6
        self.minimaleRange = param7
        self.maximaleRange = param8
        self.criticalHitProbability = param9
        self.needsFreeCell = param10
        self.needsTakenCell = param11
        self.needsVisibleEntity = param12
        self.maxEffectsStack = param13

    def getCriticalEffectById(self, spellEffectId: int) -> "HaxeSpellEffect":
        for effect in self._criticalEffects:
            if effect.id == spellEffectId:
                return effect
        return None
