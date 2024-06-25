import math
from typing import List

from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdHelper import ActionIdHelper
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.castSpellManager.SpellManager import SpellManager
from pydofus2.damageCalculation.fighterManagement.HaxeBuff import HaxeBuff
from pydofus2.damageCalculation.fighterManagement.IFighterData import IFighterData
from pydofus2.damageCalculation.fighterManagement.playerTypeEnum import PlayerTypeEnum
from pydofus2.mapTools import MapTools
from pydofus2.mx.utils.LinkedList import LinkedList


class HaxeFighter:
    MAX_RESIST_HUMAN = 50
    MAX_RESIST_MONSTER = 100
    INVALID_ID = 0
    BOMB_BREED_ID = [3112, 3113, 3114, 5161]
    STEAMER_TURRET_BREED_ID = [3287, 3288, 3289, 5143, 5141, 5142]
    MIN_PERMANENT_DAMAGE_PERCENT = 0
    BASE_PERMANENT_DAMAGE_PERCENT = 10
    MAX_PERMANENT_DAMAGE_PERCENT = 50

    def __init__(
        self,
        fighter_id: float,
        level: int,
        breed: int,
        player_type: PlayerTypeEnum,
        team_id: int,
        is_static_element: bool,
        buffs: List[HaxeBuff],
        fighter_data: IFighterData,
        is_summon_cast_previewed: bool = False,
    ):
        self.totalEffects = []  # Assuming List is a Python list for simplicity
        self.teamId = team_id
        self.playerType = player_type
        self.pendingEffects = []  # Same assumption as totalEffects
        self.level = level
        self.lastTheoreticalRawDamageTaken = None  # Placeholder for DamageRange
        self.lastRawDamageTaken = None  # Placeholder for DamageRange
        self.isSummonCastPreviewed = is_summon_cast_previewed
        self.isStaticElement = is_static_element
        self.id = fighter_id
        self.data = fighter_data
        self.breed = breed
        self.beforeLastSpellPosition = -1
        self._turnBeginPosition = -1
        self._save = None
        self._pendingPreviousPosition = -1
        self._pendingDispelledBuffs = LinkedList()
        self._pendingBuffHead = None
        self._currentPosition = -1
        self._carriedFighter = None  # Assuming HaxeFighter or None
        self._buffs = LinkedList()
        for buff in buffs:
            self._buffs.append(buff)  # Assuming this method exists for LinkedList

    def wasTeleportedInInvalidCellThisTurn(self, param1):
        for effect_output in self.pendingEffects:
            if effect_output.movement is not None and not param1.map.isCellWalkable(
                effect_output.movement.newPosition
            ):
                return True
        return False

    def wasTelefraggedThisTurn(self):
        for effect_output in self.pendingEffects:
            if effect_output.movement is not None and effect_output.movement.swappedWith is not None:
                return True
        return False

    def updateStatWithPercentValue(self, param1, param2, param3):
        modifier = 1 if param3 else -1
        total = param1.get_total()
        change = math.floor(modifier * param2)
        return int(math.floor(total + change))

    def updateStatFromFlatValue(self, param1, param2, param3):
        modifier = 1 if param3 else -1
        is_linear_buff = ActionIdHelper.isLinearBuffActionIds(param1.get_id())
        total = param1.get_total()
        if is_linear_buff:
            change = param2 * modifier
            result = total + change
        else:
            percent_change = int(math.floor(100 * (1 + modifier * param2 * 0.01))) - 100
            if total == 0:
                result = percent_change
            else:
                result = math.floor(total * (1 + percent_change * 0.01))
        return result

    def updateStatFromBuff(self, param1, param2):
        spell_effect = param1.effect
        if not SpellManager().isInstantaneousSpellEffect(spell_effect):
            return None
        stat_id = ActionIdHelper.getStatIdFromStatActionId(spell_effect.actionId)
        if stat_id == -1:
            return None
        stat = self.data.getStat(stat_id)
        if stat is None:
            stat = HaxeSimpleStat(stat_id, 0)
            self.data.setStat(stat)
        stat.updateStatFromEffect(spell_effect, param2)
        return EffectOutput.fromStatUpdate(self.id, stat.get_id(), stat.get_total())

    def underMaximizeRollEffect(self):
        for buff in self._buffs:
            if buff.effect.actionId == 782:
                return True
        return False

    def storeSpellEffectStatBoost(self, param1, param2):
        _loc3_ = param2.clone()
        _loc4_ = ActionIdHelper.statBoostToBuffActionId(param2.actionId)
        _loc3_.actionId = _loc4_
        _loc5_ = HaxeBuff(self.id, param1, _loc3_)
        return self.storePendingBuff(_loc5_)

    def storePendingBuff(self, param1):
        if param1.spell.maxEffectsStack != -1:

            def comparator(buff1, buff2):
                if buff1.effect.id != buff2.effect.id:
                    if buff1.spell.id == buff2.spell.id and buff1.effect.actionId == buff2.effect.actionId:
                        if not (buff1.effect.order == buff2.effect.order and buff1.effect.level != buff2.effect.level):
                            return buff1.effect.isCritical != buff2.effect.isCritical
                    return False
                return True

            count_before = sum(1 for buff in self._buffs if comparator(param1, buff) and buff != self._pendingBuffHead)
            count_after = sum(1 for buff in self._buffs if comparator(param1, buff) and buff == self._pendingBuffHead)

            if count_before + count_after >= param1.spell.maxEffectsStack:
                for buff_node in self._buffs:
                    if comparator(buff_node.item, param1):
                        if buff_node != self._pendingBuffHead:
                            self._pendingDispelledBuffs.add(buff_node.item)
                        self.safeRemoveBuff(buff_node)
                        break
        return self.addPendingBuff(param1)

    def setCurrentPositionCell(self, param1):
        self._pendingPreviousPosition = self.getCurrentPositionCell()
        self._currentPosition = param1
        if self.hasState(3) and self._carriedFighter is not None:
            self._carriedFighter.setCurrentPositionCell(param1)

    def setBeforeLastSpellPosition(self, param1):
        self.beforeLastSpellPosition = param1

    def savePositionBeforeSpellExecution(self):
        self.setBeforeLastSpellPosition(self.getCurrentPositionCell())

    def savePendingEffects(self):
        if self.totalEffects is not None and self.pendingEffects is not None:
            self.totalEffects = self.totalEffects + self.pendingEffects
        else:
            self.totalEffects = self.pendingEffects
        self.pendingEffects = []

    def save(self):
        self._save = {
            "id": self.id,
            "outputs": [effect for effect in self.pendingEffects],
            "buffs": self._buffs.copy(),
            "cell": self.getCurrentPositionCell(),
            "previousPosition": self._pendingPreviousPosition,
        }
        return self._save

    def safeRemoveBuff(self, param1):
        if ActionIdHelper.isStatModifier(param1.item.effect.actionId):
            isBuff = ActionIdHelper.isBuff(param1.item.effect.actionId)
            self.updateStatFromBuff(param1.item, not isBuff)
        if param1 == self._pendingBuffHead:
            self._pendingBuffHead = param1.next
        self._buffs.remove(param1)

    def resetToInitialState(self):
        self.lastRawDamageTaken = None
        self.setCurrentPositionCell(-1)
        self.setBeforeLastSpellPosition(-1)
        self._pendingPreviousPosition = -1
        self.flushPendingBuffs()
        self.pendingEffects = []
        for buff_node in self._buffs:
            buff_node.item._triggerCount = buff_node.item._startingTriggerCount

    def getCurrentPositionCell(self):
        if MapTools.isValidCellId(self._currentPosition):
            return self._currentPosition
        return self.data.getStartedPositionCell()
