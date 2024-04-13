from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.DetailedStats import DetailedStat
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStat import EntityStat
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.UsableStat import UsableStat
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.spell.SpellModifierValueTypeEnum import (
    SpellModifierValueTypeEnum,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import SpellModifiersManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdHelper import ActionIdHelper
from pydofus2.com.ankamagames.dofus.network.enums.GameActionFightInvisibilityStateEnum import (
    GameActionFightInvisibilityStateEnum,
)
from pydofus2.com.ankamagames.dofus.network.enums.SpellModifierTypeEnum import SpellModifierTypeEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacterInformations import (
    GameFightCharacterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import (
    GameFightMonsterInformations,
)
from pydofus2.damageCalculation.fighterManagement.fighterStats.HaxeStat import HaxeStat
from pydofus2.damageCalculation.fighterManagement.IFighterData import IFighterData
from pydofus2.damageCalculation.tools.StatIds import StatIds
from pydofus2.mapTools import MapTools


class FighterDataTranslator(IFighterData):
    def __init__(self, fighterInfos, fighterId):
        super().__init__()
        self._fighterInfos: GameFightFighterInformations = fighterInfos
        self._id = fighterId
        self._stats = {}
        self.resetStats()

        if isinstance(self._fighterInfos, GameFightMonsterInformations):
            monsterInfos = self._fighterInfos
            self._monsterProperties = Monster.getMonsterById(monsterInfos.creatureGenericId)

    def getUsedPM(self):
        stats = StatsManager().getStats(self._fighterInfos.contextualId)
        return stats.getStatUsedValue(StatIds.MOVEMENT_POINTS) if stats is not None else 0

    def isSummon(self):
        return self._fighterInfos.stats.summoned

    def useSummonSlot(self):
        return bool(self._monsterProperties) and self._monsterProperties.useSummonSlot

    def getSummonerId(self):
        return self._fighterInfos.stats.summoner

    def isInvisible(self):
        return self._fighterInfos.stats.invisibilityState == GameActionFightInvisibilityStateEnum.INVISIBLE

    def getBreed(self):
        if isinstance(self._fighterInfos, GameFightCharacterInformations):
            return self._fighterInfos.breed
        elif isinstance(self._fighterInfos, GameFightMonsterInformations):
            return self._fighterInfos.creatureGenericId
        return -1

    def isAlly(self):
        entities = Kernel().fightEntitiesFrame.entities
        fighter = entities.get(self._id)
        if fighter is None:
            return False
        playerId = PlayedCharacterManager().id
        return entities.get(playerId) and entities[playerId].spawnInfo.teamId == fighter.spawnInfo.teamId

    def getCharacteristicValue(self, statId):
        statKey = str(statId)
        stat = self._stats.get(statKey)
        return stat.total if stat else 0

    def resolveDodge(self):
        return -1

    def canBreedSwitchPos(self):
        return not (self._monsterProperties and not self._monsterProperties.canSwitchPos)

    def canBreedSwitchPosOnTarget(self):
        return not (self._monsterProperties and not self._monsterProperties.canSwitchPosOnTarget)

    def canBreedUsePortals(self):
        return not (self._monsterProperties and not self._monsterProperties.canUsePortal)

    def canBreedBePushed(self):
        return not (self._monsterProperties and not self._monsterProperties.canBePushed)

    def canBreedBeCarried(self):
        return not (self._monsterProperties and not self._monsterProperties.canBeCarried)

    def getStartedPositionCell(self):
        return self._fighterInfos.disposition.cellId

    def getTurnBeginPosition(self):
        # Assuming FightContextFrame and Kernel.getWorker().getFrame method exists
        fightContextFrame = Kernel().fightContextFrame
        return fightContextFrame.getFighterRoundStartPosition(self._id)

    def getPreviousPosition(self):
        fcf = Kernel().fightContextFrame
        if fcf and fcf.getFighterPreviousPosition(self._id) != MapTools.INVALID_CELL_ID:
            return fcf.getFighterPreviousPosition(self._id)
        if self._fighterInfos.previousPositions and len(self._fighterInfos.previousPositions) > 0:
            return self._fighterInfos.previousPositions[0]
        return MapTools.INVALID_CELL_ID

    def getStat(self, statId):
        statKey = str(statId)
        return self._stats.get(statKey)

    def setStat(self, stat):
        self._stats[str(stat.id)] = stat

    def getStatIds(self):
        return [stat.id for stat in self._stats.values()]

    def resetStats(self):
        self._stats = {}
        stats = StatsManager().getStats(self._id)
        if stats is not None:
            for stat in stats.stats:
                if isinstance(stat, UsableStat):
                    self._stats[stat.id] = HaxeUsableStat(
                        stat.id,
                        stat.baseValue,
                        stat.additionalValue,
                        stat.objectsAndMountBonusValue,
                        stat.alignGiftBonusValue,
                        stat.contextModifValue,
                        stat.usedValue,
                    )
                elif isinstance(stat, DetailedStat):
                    self._stats[stat.id] = HaxeDetailedStat(
                        stat.id,
                        stat.baseValue,
                        stat.additionalValue,
                        stat.objectsAndMountBonusValue,
                        stat.alignGiftBonusValue,
                        stat.contextModifValue,
                    )
                elif isinstance(stat, EntityStat):
                    self._stats[stat.id] = HaxeSimpleStat(stat.id, stat.totalValue)

    def getHealthPoints(self):
        return (
            self.getMaxHealthPoints()
            + self.getCharacteristicValue(StatIds.CUR_LIFE)
            + self.getCharacteristicValue(StatIds.CUR_PERMANENT_DAMAGE)
        )

    def getMaxHealthPoints(self):
        vitalityStat = self._stats.get(StatIds.VITALITY)
        effectiveVitality = 0
        if isinstance(vitalityStat, HaxeDetailedStat):
            effectiveVitality = (
                max(
                    0,
                    vitalityStat.base
                    + vitalityStat.objectsAndMountBonus
                    + vitalityStat.additional
                    + vitalityStat.alignGiftBonus,
                )
                + vitalityStat.contextModif
            )
        elif isinstance(vitalityStat, HaxeStat):
            effectiveVitality = vitalityStat.total
        return (
            self.getCharacteristicValue(StatIds.LIFE_POINTS)
            + effectiveVitality
            - self.getCharacteristicValue(StatIds.CUR_PERMANENT_DAMAGE)
        )

    def getBaseDamageHealEquipmentSpellMod(self, spellId):
        return SpellModifiersManager().getSpecificModifiedInt(
            self._id, spellId, SpellModifierTypeEnum.BASE_DAMAGE, SpellModifierValueTypeEnum.EQUIPMENT
        )

    def getDamageHealEquipmentSpellMod(self, spellId, actionId):
        if ActionIdHelper.isHeal(actionId):
            return SpellModifiersManager().getSpecificModifiedInt(
                self._id, spellId, SpellModifierTypeEnum.HEAL_BONUS, SpellModifierValueTypeEnum.EQUIPMENT
            )
        return SpellModifiersManager().getSpecificModifiedInt(
            self._id, spellId, SpellModifierTypeEnum.DAMAGE, SpellModifierValueTypeEnum.EQUIPMENT
        )
