from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.WeaponWrapper import WeaponWrapper
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdHelper import ActionIdHelper
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import BasicBuff
from pydofus2.damageCalculation.fighterManagement.HaxeSpellEffect import HaxeSpellEffect


class SpellEffectTranslator(HaxeSpellEffect):
    _cache = {}

    def __init__(
        self,
        id,
        level,
        order,
        actionId,
        param1,
        param2,
        param3,
        duration,
        isCritical,
        trigger,
        rawZone,
        mask,
        randomWeight,
        randomGroup,
        isDispellable,
        delay,
        category,
    ):
        super().__init__(
            id,
            level,
            order,
            actionId,
            param1,
            param2,
            param3,
            duration,
            isCritical,
            trigger,
            rawZone,
            mask,
            randomWeight,
            randomGroup,
            isDispellable,
            delay,
            category,
        )
        if id != 0:
            self._cache[self.getCacheKey(id, actionId)] = self

    @staticmethod
    def fromSpell(effect: EffectInstance, level, isCritical):
        cacheKey = SpellEffectTranslator.getCacheKey(effect.effectUid, effect.effectId)
        if effect.effectUid != 0 and cacheKey in SpellEffectTranslator._cache:
            return SpellEffectTranslator._cache[cacheKey]
        return SpellEffectTranslator(
            effect.effectUid,
            level,
            effect.order,
            effect.effectId,
            int(effect.parameter0),
            int(effect.parameter1),
            int(effect.parameter2),
            effect.duration,
            isCritical,
            effect.triggers or "I",
            effect.rawZone or "P",
            effect.targetMask or "A,a",
            effect.random,
            effect.group,
            effect.dispellable == EffectInstance.IS_DISPELLABLE,
            effect.delay,
            effect.category,
        )

    @staticmethod
    def clearCache():
        SpellEffectTranslator._cache = {}

    @staticmethod
    def fromBuff(buff: BasicBuff, level):
        return SpellEffectTranslator(
            buff.effect.effectUid,
            level,
            buff.effect.order,
            buff.effect.effectId,
            int(buff.param1),
            int(buff.param2),
            int(buff.param3),
            buff.effect.duration,
            False,
            buff.effect.triggers or "I",
            buff.effect.rawZone or "P",
            buff.effect.targetMask or "A,a",
            buff.effect.random,
            buff.effect.group,
            buff.effect.dispellable == EffectInstance.IS_DISPELLABLE,
            buff.effect.delay,
            buff.effect.category,
        )

    @staticmethod
    def fromWeapon(effect: EffectInstance, weapon: WeaponWrapper, isCritical):
        from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.DamagePreview import DamagePreview

        zone = effect.rawZone
        param0 = int(effect.parameter0)
        param1 = int(effect.parameter1)
        param2 = int(effect.parameter2)
        if param0 > 0 and param1 == 0:
            param1 = param0
        if effect.zoneShape == 0:
            zone = "P1,"
        else:
            zone = chr(effect.zoneShape) + str(effect.zoneSize or 1) + ","
        if weapon:
            if weapon.type.id == DataEnum.ITEM_TYPE_HAMMER:
                zone += str(effect.zoneMinSize or 0) + ","
            zone += str(effect.zoneEfficiencyPercent or 25) + "," + str(effect.zoneMaxEfficiency or 1)
            if isCritical and ActionIdHelper.isDamage(effect.category, effect.effectId):
                param0 += weapon.criticalHitBonus
                param1 += weapon.criticalHitBonus
        return SpellEffectTranslator(
            DamagePreview.WEAPON_EFFECTS_INDEX + 1,
            1,
            effect.order,
            effect.effectId,
            param0,
            param1,
            param2,
            effect.duration,
            isCritical,
            effect.triggers or "I",
            zone,
            "A,g",
            effect.random,
            effect.group,
            effect.dispellable == EffectInstance.IS_DISPELLABLE,
            effect.delay,
            effect.category,
        )

    @staticmethod
    def getCacheKey(id, actionId):
        return f"{id}|{actionId}"

    def getMinRoll(self):
        if self.param1 == 0 and self.param2 == 0:
            return self.param3
        return self.param1

    def getMaxRoll(self):
        return self.param2 if self.param2 != 0 else self.getMinRoll()
