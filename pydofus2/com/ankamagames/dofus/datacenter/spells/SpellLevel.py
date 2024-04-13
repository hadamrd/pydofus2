from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceDice import (
        EffectInstanceDice,
    )
    from pydofus2.com.ankamagames.dofus.datacenter.spells.EffectZone import EffectZone

import pydofus2.com.ankamagames.dofus.datacenter.spells.Spell as spellmod
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.ICellZoneProvider import ICellZoneProvider
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.IZoneShape import IZoneShape
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.ZoneEffect import ZoneEffect


class SpellLevel(ICellZoneProvider, IDataCenter):

    MODULE: str = "SpellLevels"

    id: int

    spellId: int

    grade: int

    spellBreed: int

    apCost: int

    minRange: int

    range: int

    castInLine: bool

    castInDiagonal: bool

    castTestLos: bool

    criticalHitProbability: int

    needFreeCell: bool

    needTakenCell: bool

    needFreeTrapCell: bool

    rangeCanBeBoosted: bool

    maxStack: int

    maxCastPerTurn: int

    maxCastPerTarget: int

    minCastInterval: int

    initialCooldown: int

    globalCooldown: int

    minPlayerLevel: int

    hideEffects: bool

    hidden: bool

    playAnimation: bool

    stateCriterion: str

    statesAuthorized: list[int]

    statesForbidden: list[int]

    effects: list["EffectInstanceDice"]

    criticalEffect: list["EffectInstanceDice"]

    additionalEffectsZones: list[str]

    _spell: spellmod.Spell

    _spellZoneEffects: list[IZoneShape]

    previewZones: list["EffectZone"]

    def __init__(self):
        super().__init__()

    @classmethod
    def getLevelById(cls, id: int) -> "SpellLevel":
        return GameData().getObject(cls.MODULE, id)

    idAccessors: IdAccessors = IdAccessors(getLevelById, None)

    @property
    def spell(self) -> spellmod.Spell:
        if not self._spell:
            self._spell = spellmod.Spell.getSpellById(self.spellId)
        return self._spell

    @property
    def minimalRange(self) -> int:
        return self.minRange

    @minimalRange.setter
    def minimalRange(self, pMinRange: int) -> None:
        self.minRange = pMinRange

    @property
    def maximalRange(self) -> int:
        return self.range

    @maximalRange.setter
    def maximalRange(self, pRange: int) -> None:
        self.range = pRange

    @property
    def castZoneInLine(self) -> bool:
        return self.castInLine

    @castZoneInLine.setter
    def castZoneInLine(self, pCastInLine: bool) -> None:
        self.castInLine = pCastInLine

    @property
    def castZoneInDiagonal(self) -> bool:
        return self.castInDiagonal

    @castZoneInDiagonal.setter
    def castZoneInDiagonal(self, pCastInDiagonal: bool) -> None:
        self.castInDiagonal = pCastInDiagonal

    @property
    def spellZoneEffects(self) -> list[IZoneShape]:
        if not self._spellZoneEffects:
            self._spellZoneEffects = [ZoneEffect(int(e.zoneSize), e.zoneShape) for e in self.effects]
        return self._spellZoneEffects

    def hasZoneShape(self, zoneShape: int) -> bool:
        for spze in self.spellZoneEffects:
            if spze.zoneShape == zoneShape:
                return True
        return False

    @property
    def canSummon(self) -> bool:
        effect: "EffectInstanceDice" = None
        summonId: int = 0
        monsterS: Monster = None
        for effect in self.effects:
            if (
                effect.effectId == ActionIds.ACTION_CHARACTER_ADD_DOUBLE_USE_SUMMON_SLOT
                or effect.effectId == ActionIds.ACTION_SUMMON_SLAVE
            ):
                return True
            if (
                effect.effectId == ActionIds.ACTION_SUMMON_CREATURE
                or effect.effectId == ActionIds.ACTION_FIGHT_KILL_AND_SUMMON
                or effect.effectId == ActionIds.ACTION_FIGHT_KILL_AND_SUMMON_SLAVE
            ):
                summonId = effect.diceNum
                monsterS = Monster.getMonsterById(summonId)
                if monsterS and monsterS.useSummonSlot:
                    return True
        return False

    @property
    def canBomb(self) -> bool:
        for effect in self.effects:
            if effect.effectId == ActionIds.ACTION_SUMMON_BOMB:
                return True
            if (
                effect.effectId == ActionIds.ACTION_SUMMON_CREATURE
                or effect.effectId == ActionIds.ACTION_FIGHT_KILL_AND_SUMMON
                or effect.effectId == ActionIds.ACTION_FIGHT_KILL_AND_SUMMON_SLAVE
            ):
                summonId = effect.diceNum
                monsterS = Monster.getMonsterById(summonId)
                if monsterS and monsterS.useBombSlot:
                    return True
        return False

    @property
    def canThrowPlayer(self) -> bool:
        for effect in self.effects:
            if effect.effectId == ActionIds.ACTION_THROW_CARRIED_CHARACTER:
                return True
        return False
