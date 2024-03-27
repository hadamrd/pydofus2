import math
from functools import lru_cache
from typing import TYPE_CHECKING, Any

from pydofus2.com.ankamagames.berilia.types.messages.managers.SlotDataHolderManager import \
    SlotDataHolderManager
from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdHelper import \
    ActionIdHelper
from pydofus2.com.ankamagames.dofus.network.enums.SpellModifierActionTypeEnum import \
    SpellModifierActionTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.SpellModifierTypeEnum import \
    SpellModifierTypeEnum

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import (
        EffectInstance,
    )

import threading

import pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager as cpfm
import pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager as spellmm
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceDice import \
    EffectInstanceDice
from pydofus2.com.ankamagames.dofus.datacenter.spells.EffectZone import \
    EffectZone
from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import \
    SpellLevel
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.WeaponWrapper import \
    WeaponWrapper
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import \
    StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import \
    InventoryManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter
from pydofus2.com.ankamagames.jerakine.interfaces.ISlotData import ISlotData
from pydofus2.com.ankamagames.jerakine.interfaces.ISlotDataHolder import \
    ISlotDataHolder
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.ICellZoneProvider import \
    ICellZoneProvider
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.IZoneShape import \
    IZoneShape
from pydofus2.damageCalculation.tools.StatIds import StatIds

lock = threading.Lock()


class SpellWrapper(ISlotData, ICellZoneProvider, IDataCenter):

    _cache = {}
    _cac = dict[str, "SpellWrapper"]()
    _playersCache: dict = dict[int, dict]()

    BASE_DAMAGE_EFFECT_IDS: list = [
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_BASED_ON_MOVEMENT_POINTS_FROM_AIR,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_BASED_ON_MOVEMENT_POINTS_FROM_EARTH,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_BASED_ON_MOVEMENT_POINTS_FROM_FIRE,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_BASED_ON_MOVEMENT_POINTS_FROM_WATER,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_FROM_AIR,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_FROM_BEST_ELEMENT,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_FROM_EARTH,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_FROM_FIRE,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_FROM_WATER,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_FROM_WORST_ELEMENT,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_NO_BOOST,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_NO_BOOST_FROM_AIR,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_NO_BOOST_FROM_EARTH,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_NO_BOOST_FROM_FIRE,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_LOST_NO_BOOST_FROM_WATER,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_STEAL,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_STEAL_FROM_AIR,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_STEAL_FROM_BEST_ELEMENT,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_STEAL_FROM_EARTH,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_STEAL_FROM_FIRE,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_STEAL_FROM_WATER,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_STEAL_FROM_WORST_ELEMENT,
        ActionIds.ACTION_CHARACTER_LIFE_POINTS_STEAL_WITHOUT_BOOST,
        ActionIds.ACTION_CHARACTER_MANA_USE_KILL_LIFE_AIR,
        ActionIds.ACTION_CHARACTER_MANA_USE_KILL_LIFE_FIRE,
        ActionIds.ACTION_CHARACTER_MANA_USE_KILL_LIFE_WATER,
        ActionIds.ACTION_CHARACTER_MOVEMENT_USE_KILL_LIFE_AIR,
        ActionIds.ACTION_CHARACTER_MOVEMENT_USE_KILL_LIFE_EARTH,
        ActionIds.ACTION_CHARACTER_MOVEMENT_USE_KILL_LIFE_FIRE,
        ActionIds.ACTION_CHARACTER_MOVEMENT_USE_KILL_LIFE_NEUTRAL,
        ActionIds.ACTION_CHARACTER_MOVEMENT_USE_KILL_LIFE_WATER,
    ]

    def __init__(self):
        self._uri: str = None
        self._slotDataHolderManager: SlotDataHolderManager = None
        self._canTargetCasterOutOfZone: object = None
        self._variantActivated: bool = False
        self._spellLevel: SpellLevel = None
        self._spell: Spell = None
        self.id: int = 0
        self.spellLevel: int = 1
        self.effects = list["EffectInstance"]()
        self.criticalEffect = list["EffectInstance"]()
        self.gfxId: int = 0
        self.playerId: float = 0
        self.versionNum: int = 0
        self.additionalEffectsZones = list[EffectZone]()
        self._actualCooldown: int = 0
        self._entityId = PlayedCharacterManager().id
        super().__init__()

    @classmethod
    @lru_cache(maxsize=64, typed=False)
    def getSpellCached(cls, spellID: int, playerId: float = 0) -> "SpellWrapper":
        return cls.getSpell(spellID, playerId)

    @classmethod
    def getSpell(cls, spellID: int, playerId: float = 0) -> "SpellWrapper":
        spell = SpellWrapper()
        spell.id = spellID
        spell._slotDataHolderManager = SlotDataHolderManager(spell)
        spell.playerId = playerId
        return spell

    @classmethod
    def thname(cls):
        return threading.current_thread().name

    @classmethod
    def create(
        cls,
        spellID: int,
        spellLevel: int = 0,
        useCache: bool = True,
        playerId: float = 0,
        variantActivated: bool = False,
        areModifiers: bool = True,
    ) -> "SpellWrapper":
        with lock:
            spell = None
            if spellID == 0:
                useCache = False
            if useCache:
                spell = cls.getSpellCached(spellID, playerId)
            else:
                spell = cls.getSpell(spellID, playerId)
            if spell is None:
                raise Exception("Something went wrong when creating spell")
            if spellID == 0 and cls._cac.get(cls.thname()) is not None:
                spell = cls._cac.get(cls.thname())
            else:
                if spellID == 0:
                    cls._cac[cls.thname()] = spell
                spell.id = spellID
                spell.gfxId = spellID
                spell.variantActivated = variantActivated
            spellData: Spell = Spell.getSpellById(spellID)
            if not spellData:
                raise Exception("Spell not found")
            if spellLevel == 0:
                spell.updateSpellLevelAccordingToPlayerLevel()
            else:
                spell.spellLevel = spellLevel
                spell._spellLevel = spellData.getSpellLevel(spell.spellLevel)
            spell.setSpellEffects(areModifiers)
        return spell

    @classmethod
    def getSpellWrapperById(cls, spellId: int, playerID: float, forceCreate: bool = False) -> "SpellWrapper":
        if forceCreate:
            return cls.create(spellId)
        if playerID != 0:
            if playerID not in cls._playersCache:
                return None
            if not cls._playersCache[playerID].get(spellId) and cls._cache.get(spellId):
                cls._playersCache[playerID][spellId] = cls._cache[spellId].clone()
            if spellId == 0:
                return cls._cac[cls.thname()]
            if spellId in cls._playersCache[playerID]:
                return cls._playersCache[playerID][spellId]
            return None
        return cls._cache[spellId]

    @classmethod
    def refreshAllPlayerSpellHolder(cls, playerId: float) -> None:
        cls.refreshSpellHolders(playerId)

    @classmethod
    def refreshSpellHolders(cls, playerID: float) -> None:
        wrapper: SpellWrapper = None
        for wrapper in cls._playersCache.get(playerID, dict()).values():
            if wrapper:
                wrapper._slotDataHolderManager.refreshAll()
        if cls._cac.get(cls.thname()):
            cls._cac[cls.thname()]._slotDataHolderManager.refreshAll()

    @classmethod
    def resetAllCoolDown(cls, playerId: float, accessKey: object) -> None:
        cls.getSpellCached.cache_clear()

    @classmethod
    def removeAllSpellWrapperBut(cls, playerId: float, accessKey: object) -> None:
        temp: list = []
        for id in cls._playersCache:
            if float(id) != playerId:
                temp.append(id)
        num = len(temp)
        i = 0
        while i < num:
            del cls._playersCache[temp[i]]
            i += 1

    def removeAllSpellWrapper(self) -> None:
        self._playersCache = dict()
        self._cache = []

    @property
    def actualCooldown(self) -> int:
        return self._actualCooldown if PlayedCharacterManager().isFighting else 0

    @actualCooldown.setter
    def actualCooldown(self, u: int) -> None:
        self._actualCooldown = u
        self._slotDataHolderManager.refreshAll()

    @property
    def spellLevelInfos(self) -> SpellLevel:
        return self._spellLevel

    def updateSpellLevelAndEffectsAccordingToPlayerLevel(self) -> None:
        self.updateSpellLevelAccordingToPlayerLevel()
        self.setSpellEffects()

    @property
    def variantActivated(self) -> bool:
        return self._variantActivated

    @variantActivated.setter
    def variantActivated(self, value: bool) -> None:
        self._variantActivated = value

    @property
    def maximalRange(self) -> int:
        return self.spellLevelInfos.range

    @property
    def minimalRange(self) -> int:
        return self["minRange"]

    @property
    def castZoneInLine(self) -> bool:
        return self["castInLine"]

    @property
    def castZoneInDiagonal(self) -> bool:
        return self["castInDiagonal"]

    @property
    def spellZoneEffects(self) -> list[IZoneShape]:
        if InventoryManager().currentBuildId != -1:
            for build in InventoryManager().builds:
                if build.id == InventoryManager().currentBuildId:
                    break
            if self.id == 0:
                for iw in build.equipment:
                    if isinstance(iw, WeaponWrapper):
                        break
                if not isinstance(iw, WeaponWrapper) and self.spellLevelInfos:
                    return self.spellLevelInfos.spellZoneEffects
        if self.id != 0 or not PlayedCharacterManager().currentWeapon:
            if self.spellLevelInfos:
                return self.spellLevelInfos.spellZoneEffects
        return None

    @property
    def hideEffects(self) -> bool:
        if self.id == 0 and PlayedCharacterManager().currentWeapon is not None:
            return PlayedCharacterManager().currentWeapon.hideEffects
        if self.spellLevelInfos:
            return self.spellLevelInfos.hideEffects
        return False

    @property
    def info1(self) -> str:
        if self.actualCooldown == 0 or not PlayedCharacterManager().isFighting:
            return None
        if self.actualCooldown == 63:
            return "-"
        return str(self.actualCooldown)

    @property
    def startTime(self) -> int:
        return 0

    @property
    def endTime(self) -> int:
        return 0

    @endTime.setter
    def endTime(self, t: int) -> None:
        pass

    @property
    def timer(self) -> int:
        return 0

    @property
    def active(self) -> bool:
        if not PlayedCharacterManager().isFighting:
            return True
        canCast, _ = cpfm.CurrentPlayedFighterManager().canCastThisSpell(self.spellId, self.spellLevel)
        return canCast

    @property
    def spell(self) -> Spell:
        if not self._spell:
            self._spell = Spell.getSpellById(self.id)
        return self._spell

    @property
    def spellId(self) -> int:
        if self.spell:
            return self.spell.id
        return 0

    def getEntityId(self):
        if not math.isnan(self.playerId) and self.playerId != 0:
            return self.playerId
        from pydofus2.com.ankamagames.dofus.uiApi.PlayedCharacterApi import \
            PlayedCharacterApi

        if PlayedCharacterApi().isInFight():
            return cpfm.CurrentPlayedFighterManager().currentFighterId
        return PlayedCharacterManager().id

    @property
    def criticalHitProbability(self):
        entityId = self.getEntityId()
        criticalHitProbability = self.baseCriticalHitProbability
        stats = None
        if not math.isnan(entityId):
            criticalHitProbability = spellmm.SpellModifiersManager().getModifiedInt(
                entityId,
                self.id,
                SpellModifierTypeEnum.CRITICAL_HIT_BONUS,
                criticalHitProbability,
            )
            if criticalHitProbability > 0:
                stats = StatsManager().getStats(entityId)
        if stats is not None:
            criticalHitProbability += stats.getStatTotalValue(StatIds.CRITICAL_HIT)
        criticalHitProbability = max(0, criticalHitProbability)
        return min(criticalHitProbability, 100)

    @property
    def isMaxRangeModifiableWithStats(self):
        return self.spellLevelInfos.rangeCanBeBoosted

    @property
    def isMaxRangeModifiableWithStatsWithModifiers(self):
        return spellmm.SpellModifiersManager().getModifiedBool(
            self.getEntityId(),
            self.id,
            SpellModifierTypeEnum.RANGEABLE,
            self.isMaxRangeModifiableWithStats,
        )

    @property
    def maxRange(self):
        entityId = self.getEntityId()
        stats = StatsManager().getStats(entityId)
        spellModifiers = spellmm.SpellModifiersManager().getSpellModifiers(entityId, self.id)
        finalRange = self.maximalRange

        if spellModifiers is not None:
            if spellModifiers.hasAction(SpellModifierTypeEnum.RANGE_MAX, SpellModifierActionTypeEnum.ACTION_SET):
                return spellModifiers.getModifiedInt(SpellModifierTypeEnum.RANGE_MAX)
            finalRange = spellModifiers.getModifiedInt(SpellModifierTypeEnum.RANGE_MAX, finalRange)

        if self.isMaxRangeModifiableWithStatsWithModifiers and stats is not None:
            rangeBonus = stats.getStatTotalValue(StatIds.RANGE) - stats.getStatAdditionalValue(StatIds.RANGE)
            finalRange += rangeBonus

        if finalRange < self.minimalRange:
            finalRange = self.minimalRange

        return int(finalRange)

    @property
    def previewZones(self) -> list[EffectZone]:
        if self._spellLevel is None:
            return None
        return self._spellLevel.previewZones

    @property
    def canTargetCasterOutOfZone(self) -> bool:
        effect: "EffectInstance" = None
        if self._canTargetCasterOutOfZone == None:
            for effect in self.effects:
                if effect.targetMask.find("C") != -1 and effect.triggers == "I":
                    self._canTargetCasterOutOfZone = True
            if not self._canTargetCasterOutOfZone:
                for effect in self.criticalEffect:
                    if effect.targetMask.find("C") != -1 and effect.triggers == "I":
                        self._canTargetCasterOutOfZone = True
            if not self._canTargetCasterOutOfZone:
                self._canTargetCasterOutOfZone = False
        return self._canTargetCasterOutOfZone

    def __getitem__(self, name) -> Any:
        if hasattr(self, name):
            return getattr(self, name)

        if InventoryManager().currentBuildId != -1:
            for build in InventoryManager().builds:
                if build.id == InventoryManager().currentBuildId:
                    break
            if self.id == 0:
                for iw in build.equipment:
                    if isinstance(iw, WeaponWrapper):
                        break
                if isinstance(iw, WeaponWrapper):
                    return self.getWeaponProperty(name, iw)

        elif self.id == 0 and PlayedCharacterManager().currentWeapon != None:
            return self.getWeaponProperty(name)

        if str(name) in [
            "id",
            "nameId",
            "descriptionId",
            "typeId",
            "scriptParams",
            "scriptParamsCritical",
            "scriptId",
            "scriptIdCritical",
            "iconId",
            "spellLevels",
            "useParamCache",
            "name",
            "description",
            "variants",
            "defaultPreviewZone",
            "effectZone",
        ]:
            return getattr(self.spell, str(name))

        elif str(name) in [
            "spellBreed",
            "needFreeCell",
            "needTakenCell",
            "minPlayerLevel",
            "maxStack",
            "globalCooldown",
        ]:
            return getattr(self.spellLevelInfos, str(name))

        if str(name) == "maxCastPerTurn":
            return spellmm.SpellModifiersManager().getModifiedInt(
                self.getEntityId(),
                self.id,
                SpellModifierTypeEnum.MAX_CAST_PER_TURN,
                self.spellLevelInfos.maxCastPerTurn,
            )

        if str(name) in ["range", "maxRange"]:
            return self.maxRange

        if str(name) == "minRange":
            return spellmm.SpellModifiersManager().getModifiedInt(
                self.getEntityId(),
                self.id,
                SpellModifierTypeEnum.RANGE_MIN,
                self.spellLevelInfos.minRange,
            )

        if str(name) == "maxCastPerTarget":
            return spellmm.SpellModifiersManager().getModifiedInt(
                self.getEntityId(),
                self.id,
                SpellModifierTypeEnum.MAX_CAST_PER_TARGET,
                self.spellLevelInfos.maxCastPerTarget,
            )

        if str(name) == "castInLine":
            return spellmm.SpellModifiersManager().getModifiedBool(
                self.getEntityId(),
                self.id,
                SpellModifierTypeEnum.CAST_LINE,
                self.spellLevelInfos.castInLine,
            )

        if str(name) == "castInDiagonal":
            return self.spellLevelInfos.castInDiagonal

        if str(name) == "castTestLos":
            return spellmm.SpellModifiersManager().getModifiedBool(
                self.getEntityId(),
                self.id,
                SpellModifierTypeEnum.LOS,
                self.spellLevelInfos.castTestLos,
            )

        if str(name) == "rangeCanBeBoosted":
            return spellmm.SpellModifiersManager().getModifiedBool(
                self.getEntityId(),
                self.id,
                SpellModifierTypeEnum.RANGEABLE,
                self.spellLevelInfos.rangeCanBeBoosted,
            )

        if str(name) == "apCost":
            return spellmm.SpellModifiersManager().getModifiedInt(
                self.getEntityId(),
                self.id,
                SpellModifierTypeEnum.AP_COST,
                self.spellLevelInfos.apCost,
            )

        if str(name) == "minCastInterval":
            return spellmm.SpellModifiersManager().getModifiedInt(
                self.getEntityId(),
                self.id,
                SpellModifierTypeEnum.CAST_INTERVAL,
                self.spellLevelInfos.minCastInterval,
            )

        if str(name) == "isSpellWeapon":
            return self.id == 0

        if str(name) == "isDefaultSpellWeapon":
            return self.id == 0 and not PlayedCharacterManager().currentWeapon

        if str(name) == "statesCriterion":
            return self.spellLevelInfos.stateCriterion

        else:
            return

    def getWeaponProperty(self, name, item: ItemWrapper = None) -> Any:
        weapon: ItemWrapper = item if item else PlayedCharacterManager().currentWeapon
        if not weapon:
            return None

        if str(name) == "id":
            return 0

        elif str(name) in [
            "nameId",
            "descriptionId",
            "iconId",
            "name",
            "description",
            "baseCriticalHitProbability",
            "criticalHitProbability",
            "castInLine",
            "castInDiagonal",
            "castTestLos",
            "apCost",
            "minRange",
            "range",
        ]:
            return getattr(weapon, name)

        if str(name) in [
            "isDefaultSpellWeapon",
            "useParamCache",
            "needTakenCell",
            "rangeCanBeBoosted",
        ]:
            return False

        if str(name) in ["isSpellWeapon", "needFreeCell"]:
            return True

        if str(name) in [
            "minCastInterval",
            "minPlayerLevel",
            "maxStack",
            "maxCastPerTurn",
            "maxCastPerTarget",
        ]:
            return 0

        if str(name) == "typeId":
            return DataEnum.SPELL_TYPE_SPECIALS

        if str(name) in ["scriptParams", "scriptParamsCritical", "spellLevels"]:
            return None

        if str(name) in ["scriptId", "scriptIdCritical", "spellBreed"]:
            return 0

        if str(name) == "variants":
            return []

        else:
            return

    @property
    def baseCriticalHitProbability(self):
        if self["isSpellWeapon"] and not self["isDefaultSpellWeapon"]:
            toReturn = self.getWeaponProperty("criticalHitProbability")
            if toReturn is None:
                return 0
            return toReturn
        return self.spellLevelInfos.criticalHitProbability

    def clone(self) -> Any:
        return SpellWrapper.create(self.id, self.spellLevel, False, self.playerId, self.variantActivated)

    def addHolder(self, h: ISlotDataHolder) -> None:
        self._slotDataHolderManager.addHolder(h)

    def setLinkedSlotData(self, slotData: ISlotData) -> None:
        self._slotDataHolderManager.setLinkedSlotData(slotData)

    def removeHolder(self, h: ISlotDataHolder) -> None:
        self._slotDataHolderManager.removeHolder(h)

    def __str__(self) -> str:
        return f"[SpellWrapper #{self.id}]"

    def updateSpellLevelAccordingToPlayerLevel(self) -> None:
        currentCharacterLevel: int = PlayedCharacterManager().limitedLevel
        if not self.spell:
            return
        spellLevels = self._spell.spellLevelsInfo
        spellLevelsCount = len(spellLevels)
        index = 0
        for i in range(spellLevelsCount - 1, -1, -1):
            if currentCharacterLevel >= spellLevels[i].minPlayerLevel:
                index = i
                break
        self._spellLevel = spellLevels[index]
        self.spellLevel = index + 1

    def setSpellEffects(self, areModifiers=True):
        entityId = self.getEntityId()
        regularBaseDamageMod = 0
        criticalBaseDamageMod = 0
        self.effects = []
        self.criticalEffect = []

        for effectInstance in self._spellLevel.effects:
            effectInstance = effectInstance.clone()
            if areModifiers and (
                effectInstance.category == DataEnum.ACTION_TYPE_DAMAGES
                and (
                    effectInstance.effectId in self.BASE_DAMAGE_EFFECT_IDS
                    or ActionIdHelper.isHeal(effectInstance.effectId)
                )
            ):
                if isinstance(effectInstance, EffectInstanceDice):
                    regularBaseDamageMod = spellmm.SpellModifiersManager().getModifiedInt(
                        entityId, self.id, SpellModifierTypeEnum.BASE_DAMAGE
                    )
                    effectInstance.diceNum += regularBaseDamageMod
                    if effectInstance.diceSide > 0:
                        effectInstance.diceSide += regularBaseDamageMod
                if ActionIdHelper.isHeal(effectInstance.effectId):
                    effectInstance.modificator = spellmm.SpellModifiersManager().getModifiedInt(
                        entityId,
                        self.id,
                        SpellModifierTypeEnum.HEAL_BONUS,
                        effectInstance.modificator,
                    )
                else:
                    effectInstance.modificator = spellmm.SpellModifiersManager().getModifiedInt(
                        entityId, self.id, SpellModifierTypeEnum.DAMAGE
                    )
            self.effects.append(effectInstance)

        for effectInstance in self._spellLevel.criticalEffect:
            effectInstance = effectInstance.clone()
            if areModifiers and (
                effectInstance.category == DataEnum.ACTION_TYPE_DAMAGES
                and (
                    effectInstance.effectId in self.BASE_DAMAGE_EFFECT_IDS
                    or ActionIdHelper.isHeal(effectInstance.effectId)
                )
            ):
                if isinstance(effectInstance, EffectInstanceDice):
                    criticalBaseDamageMod = spellmm.SpellModifiersManager().getModifiedInt(
                        entityId, self.id, SpellModifierTypeEnum.BASE_DAMAGE
                    )
                    effectInstance.diceNum += criticalBaseDamageMod
                    if effectInstance.diceSide > 0:
                        effectInstance.diceSide += criticalBaseDamageMod
                if ActionIdHelper.isHeal(effectInstance.effectId):
                    effectInstance.modificator = spellmm.SpellModifiersManager().getModifiedInt(
                        entityId,
                        self.id,
                        SpellModifierTypeEnum.HEAL_BONUS,
                        effectInstance.modificator,
                    )
                else:
                    effectInstance.modificator = spellmm.SpellModifiersManager().getModifiedInt(
                        entityId, self.id, SpellModifierTypeEnum.DAMAGE
                    )
            self.criticalEffect.append(effectInstance)
