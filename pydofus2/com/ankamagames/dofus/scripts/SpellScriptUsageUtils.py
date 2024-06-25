import random
from collections import defaultdict

from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionFactory import ItemCriterionFactory
from pydofus2.com.ankamagames.dofus.datacenter.spells.BoundScriptUsageData import BoundScriptUsageData
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.DamageUtil import DamageUtil
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.jerakine.types.zones.Custom import Custom
from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone


class SpellScriptUsageUtils:

    @staticmethod
    def isSpellLevelMatch(spell: SpellWrapper, spellLevels: list[int]):
        return not spellLevels or spell.spellLevel in spellLevels

    @staticmethod
    def isCriterionMatch(rawCriterion: str):
        if not rawCriterion:
            return True
        criterion = ItemCriterionFactory.create(rawCriterion)
        return criterion is not None and criterion.isRespected

    @staticmethod
    def isCasterMatch(casterId: float, casterMask: str):
        if not casterMask:
            return True
        relatedEffect = EffectInstance()
        relatedEffect.targetMask = casterMask
        casterPos = Kernel().fightEntitiesFrame.getLastKnownEntityPosition(casterId)
        return DamageUtil.verifySpellEffectMask(casterId, casterId, relatedEffect, casterPos)

    @staticmethod
    def generateScriptZone(
        targetZone: DisplayZone, activationZone: DisplayZone, casterId, targetedCellId, activationMask, entitiesIds
    ):
        cellIds = []
        if not activationMask:
            for cellId in activationZone.getCells(targetedCellId):
                target_cell_ids = targetZone.getCells(cellId)
                for target_cell_id in target_cell_ids:
                    cellIds.append(target_cell_id)
            return Custom(cellIds)

        activation_effect = EffectInstance()
        activation_effect.targetMask = activationMask
        activation_effect.zoneShape = targetZone.shape
        activation_effect.zoneSize = targetZone.size
        activation_effect.zoneMinSize = targetZone.otherSize

        activation_zone_cell_ids = activationZone.getCells(targetedCellId)
        fight_entities_frame = Kernel().fightEntitiesFrame

        for entity_id in entitiesIds:
            entity_info = fight_entities_frame.getEntityInfos(entity_id)
            entity_pos = entity_info.disposition.cellId
            if entity_pos in activation_zone_cell_ids:
                if DamageUtil.verifySpellEffectMask(
                    casterId, entity_id, activation_effect, entity_pos
                ):  # Placeholder for condition check
                    target_cell_ids = targetZone.getCells(entity_pos)
                    for target_cell_id in target_cell_ids:
                        cellIds.append(target_cell_id)
        return Custom(cellIds)

    @staticmethod
    def getRandomizedUsageData(allUsageData: list[BoundScriptUsageData]) -> list[BoundScriptUsageData]:
        weights = defaultdict(int)
        totalWeight = 0

        for usageData in allUsageData:
            if usageData.randomGroup > 0:
                weights[usageData.randomGroup] += usageData.random
                totalWeight += usageData.random

        randomValue = random.random() * totalWeight
        selectedGroup = -1

        for groupKey, weight in weights.items():
            if randomValue < weight:
                selectedGroup = groupKey
                break
            randomValue -= weight

        filteredUsageData = [
            usageData
            for usageData in allUsageData
            if not (usageData.randomGroup > 0 and usageData.randomGroup != selectedGroup)
        ]

        return filteredUsageData

    @staticmethod
    def isTargetMatch(
        scriptZone: Custom, casterId: float, entityInfo: GameFightFighterInformations, targetEffect: EffectInstance
    ) -> bool:
        entityCellId = entityInfo.disposition.cellId
        return (
            entityInfo.spawnInfo.alive
            and entityCellId in scriptZone.getCells()
            and DamageUtil.verifySpellEffectMask(casterId, entityInfo.contextualId, targetEffect, entityCellId)
        )
