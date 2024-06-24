from typing import List

from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import SpellLevel
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.WeaponWrapper import WeaponWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.SpellEffectTranslator import SpellEffectTranslator
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import BasicBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.TriggeredBuff import TriggeredBuff
from pydofus2.damageCalculation.DamageCalculator import DamageCalculator
from pydofus2.damageCalculation.fighterManagement.HaxeBuff import HaxeBuff
from pydofus2.damageCalculation.spellManagement.HaxeSpell import HaxeSpell


class DamagePreview:
    WEAPON_EFFECTS_INDEX = 0
    _isInit = False
    haxeSpellCache = {}
    FIST_SPELL_ID = 0

    @classmethod
    def init(cls):
        if not cls._isInit:
            haxe.initSwc()
            DamageCalculator.dataInterface = DamageCalculationTranslator()
            DamageCalculator.logger = HaxeLoggerTranslator()
            cls._isInit = True

    @classmethod
    def createHaxeSpell(cls, spell) -> "HaxeSpell":
        cacheKey = 0
        spellWrapper = None
        if isinstance(spell, SpellWrapper):
            spellWrapper = spell
            spell = spellWrapper.spellLevelInfos
        spellLevel = 1 if isinstance(spell, WeaponWrapper) else spell.grade
        spellId = spell.spellId
        isFist = spell.spellId == cls.FIST_SPELL_ID
        isWeapon = not isinstance(spell, SpellLevel) or isFist
        if isWeapon and not isFist:
            spell = PlayedCharacterManager().currentWeapon
            spellId = 0
        if not isWeapon:
            cacheKey = DamageCalculator.create32BitHashSpellLevel(spellId, spellLevel)
            if cacheKey in cls.haxeSpellCache:
                return cls.haxeSpellCache[cacheKey]
        spellEffects = spell.effects if isWeapon and not isFist else spell.effects
        spellCriticalEffects = spellEffects if isWeapon and not isFist else spell.criticalEffect
        translatedEffects = cls.loadEffectArray(spell, spellEffects, isWeapon, False)
        translatedCriticalEffects = cls.loadEffectArray(spell, spellCriticalEffects, isWeapon, True)
        canAlwaysTriggerSpells = (
            isWeapon or spell.spell.canAlwaysTriggerSpells if isinstance(spell, SpellLevel) else False
        )
        if isWeapon and not isinstance(spell, SpellLevel):
            spell = PlayedCharacterManager().currentWeapon
        needFreeCell = needTakenCell = needVisibleEntity = False
        if spellWrapper is not None:
            needFreeCell = spellWrapper.needFreeCellWithModifiers
            needTakenCell = spellWrapper.needTakenCellWithModifiers
            needVisibleEntity = spellWrapper.needVisibleEntityWithModifiers
        elif isinstance(spell, SpellLevel):
            needFreeCell = spell.needFreeCell
            needTakenCell = spell.needTakenCell
            needVisibleEntity = spell.needVisibleEntity
        return HaxeSpell(
            spellId if not isWeapon else 0,
            translatedEffects,
            translatedCriticalEffects,
            spellLevel,
            canAlwaysTriggerSpells,
            isWeapon,
            spell.minRange,
            spell.range,
            spellWrapper.criticalHitProbability if spellWrapper is not None else spell.criticalHitProbability,
            needFreeCell,
            needTakenCell,
            needVisibleEntity,
            spell.maxStack if isinstance(spell, SpellLevel) else -1,
        )

    @classmethod
    def createHaxeBuff(cls, buff: BasicBuff) -> HaxeBuff:
        casterId = buff.castingSpell.casterId
        grade = buff.castingSpell.spellLevelData.grade if buff.castingSpell.spellLevelData else 1
        spellLevel = Spell.getSpellById(buff.castingSpell.spellData.id).getSpellLevel(grade)
        newSpell = cls.createHaxeSpell(spellLevel)
        effect = SpellEffectTranslator.fromBuff(buff, spellLevel.grade)
        isCritical = newSpell.getCriticalEffectById(effect.id) is not None
        effect.isCritical = isCritical
        triggerCount = buff.triggerCount if isinstance(buff, TriggeredBuff) else -1
        return HaxeBuff(casterId, newSpell, effect, triggerCount)

    @classmethod
    def loadEffectArray(cls, spell, sourceEffects: List[EffectInstance], isWeapon: bool, isCritical: bool) -> list:
        targetEffects = []
        for effect in sourceEffects:
            if not effect.forClientOnly and effect.delay == 0:
                if isWeapon:
                    if effect.useInFight:
                        targetEffects.append(
                            SpellEffectTranslator.fromWeapon(
                                effect, PlayedCharacterManager().currentWeapon, isCritical
                            )
                        )
                elif isinstance(spell, SpellLevel):
                    targetEffects.append(SpellEffectTranslator.fromSpell(effect, spell.grade, isCritical))
        return targetEffects
