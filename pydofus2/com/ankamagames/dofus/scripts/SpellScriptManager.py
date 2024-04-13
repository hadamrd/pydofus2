from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellScript import SpellScript
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellZoneManager import SpellZoneManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastSequenceContext import SpellCastSequenceContext
from pydofus2.com.ankamagames.dofus.scripts.SpellScriptContext import SpellScriptContext
from pydofus2.com.ankamagames.dofus.scripts.SpellScriptUsageUtils import SpellScriptUsageUtils
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class SpellScriptManager(metaclass=Singleton):

    def __init__(self) -> None:
        pass

    def resolveScriptUsage(
        self, spell: SpellWrapper, isCritical, casterId, targetedCellId
    ) -> list[SpellScriptContext]:
        if targetedCellId == -1:
            return []

        spellData = spell.spell
        if spell.id == 0:
            weaponContext = SpellScriptContext()
            weaponContext.scriptId = SpellScript.WEAPON_SCRIPT_ID
            weaponContext.spellId = spell.id
            weaponContext.casterId = casterId
            weaponContext.targetedCellId = targetedCellId
            return [weaponContext]

        allUsageData = spellData.criticalHitBoundScriptUsageData if isCritical else spellData.boundScriptUsageData
        randomizedUsageData = SpellScriptUsageUtils.getRandomizedUsageData(allUsageData)
        if len(randomizedUsageData) == 0:
            return []

        if DataMapProvider().isInFight:
            entitiesFrame = Kernel().fightEntitiesFrame
        else:
            entitiesFrame = Kernel().roleplayEntitiesFrame

        entitiesIds = entitiesFrame.getEntitiesIdsList()
        scriptIds = []

        for usageData in randomizedUsageData:
            if SpellScriptUsageUtils.isSpellLevelMatch(spell, usageData.spellLevels):
                if SpellScriptUsageUtils.isCriterionMatch(usageData.criterion):
                    if SpellScriptUsageUtils.isCasterMatch(casterId, usageData.casterMask):
                        spellZoneManager = SpellZoneManager()
                        isWeapon = spell.id == 0
                        activationZone = spellZoneManager.parseZone(
                            usageData.activationZone, casterId, targetedCellId, isWeapon
                        )
                        targetZone = spellZoneManager.parseZone(
                            usageData.targetZone, casterId, targetedCellId, isWeapon
                        )
                        scriptZone = SpellScriptUsageUtils.generateScriptZone(
                            targetZone, activationZone, casterId, targetedCellId, usageData.activationMask, entitiesIds
                        )
                        if scriptZone.surface != 0:
                            if not usageData.targetMask:
                                for cellId in scriptZone.getCells():
                                    context = SpellScriptContext()
                                    context.scriptId = usageData.scriptId
                                    context.spellId = spell.id
                                    context.casterId = casterId
                                    context.targetedCellId = cellId
                                    scriptIds.append(context)
                            else:
                                targetEffectZone = spellZoneManager.getEffectZone(usageData.targetZone)
                                targetEffect = EffectInstance()
                                targetEffect.targetMask = usageData.targetMask
                                targetEffect.zoneShape = targetEffectZone.activationZoneShape
                                targetEffect.zoneSize = targetEffectZone.activationZoneSize
                                targetEffect.zoneMinSize = targetEffectZone.activationZoneMinSize
                                targetEffect.zoneStopAtTarget = targetEffectZone.activationZoneStopAtTarget
                                fightEntitiesFrame = Kernel().fightEntitiesFrame
                                for entityId in entitiesIds:
                                    entityInfo = fightEntitiesFrame.getEntityInfos(entityId)
                                    if entityInfo is not None:
                                        if SpellScriptUsageUtils.isTargetMatch(
                                            scriptZone, casterId, entityInfo, targetEffect
                                        ):
                                            context = SpellScriptContext()
                                            context.scriptId = usageData.scriptId
                                            context.spellId = spell.id
                                            context.casterId = casterId
                                            context.targetedCellId = entityInfo.disposition.cellId
                                            scriptIds.append(context)
        return scriptIds

    def resolveScriptUsageFromCastContext(
        self, castSequenceContext: SpellCastSequenceContext, specificTargetedCellId=-1
    ):
        spell = SpellWrapper.getSpellWrapperById(castSequenceContext.spellData.id, castSequenceContext.casterId)
        if spell is None:
            spell = SpellWrapper.create(
                castSequenceContext.spellData.id,
                castSequenceContext.spellLevelData.grade,
                True,
                castSequenceContext.casterId,
            )
        targetedCellId = specificTargetedCellId if specificTargetedCellId != -1 else castSequenceContext.targetedCellId
        return self.resolveScriptUsage(
            spell, castSequenceContext.isCriticalHit, castSequenceContext.casterId, targetedCellId
        )
