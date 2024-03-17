from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.DetailedStats import \
    DetailedStat
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.Stat import Stat
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.UsableStat import \
    UsableStat
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.damageCalculation.tools.StatIds import StatIds


class EntityStats:

    def __init__(self, entityId: float):
        self._entityId = entityId
        self._stats = dict[float, Stat]()

    @property
    def entityId(self) -> float:
        return self._entityId

    @property
    def stats(self) -> dict:
        return self._stats

    def getFormattedMessage(self, message: str) -> str:
        return f"[EntityStats] (Entity ID: {self._entityId}): {message}"

    def setStat(self, stat: Stat, isBulkUpdate: bool = True) -> None:
        stat.entityId = float(self._entityId)
        self._stats[float(stat.id)] = stat

    def getStat(self, statId: float) -> Stat:
        statId = float(statId)
        if statId not in self._stats:
            Logger().error(self.getFormattedMessage(f"Stat ID {statId} not found in stats"))
            return
        return self._stats[statId]

    def deleteStat(self, statId: float) -> None:
        statId = float(statId)
        if statId not in self._stats:
            return
        self._stats[statId].reset()
        del self._stats[statId]

    def resetStats(self) -> None:
        for stat in self._stats.values():
            stat.reset()
        self._stats.clear()

    def getStatsNumber(self) -> float:
        return len(self._stats)

    def hasStat(self, statId: float) -> bool:
        return float(statId) in self._stats

    def getStatTotalValue(self, statId: float) -> float:
        stat = self._stats.get(float(statId))
        return float(stat.totalValue) if stat else 0

    def getDetailedStatValue(self, statId: float, attrib: str) -> float:
        stat = self._stats.get(float(statId))
        if stat and isinstance(stat, DetailedStat):
            return getattr(stat, attrib)
        return 0
    
    def getStatBaseValue(self, statId: float) -> float:
        return self.getDetailedStatValue(statId, "baseValue")

    def getStatAdditionalValue(self, statId: float) -> float:
        return self.getDetailedStatValue(statId, "additionalValue")

    def getStatObjectsAndMountBonusValue(self, statId: float) -> float:
        return self.getDetailedStatValue(statId, "objectsAndMountBonusValue")

    def getStatAlignGiftBonusValue(self, statId: float) -> float:
        return self.getDetailedStatValue(statId, "alignGiftBonusValue")

    def getStatContextModifValue(self, statId: float) -> float:
        return self.getDetailedStatValue(statId, "contextModifValue")
    
    def getStatUsedValue(self, statId: float) -> float:
        stat = self._stats[float(statId)]
        if stat and isinstance(stat, UsableStat):
            return stat.usedValue
        return 0

    def __str__(self) -> str:
        statsDump = ""
        for stat in self._stats.values():
            statsDump += "\n\t" + str(stat)
        if not statsDump:
            statsDump = "\n\tNo stats to display."
        return self.getFormattedMessage(statsDump)

    def getHealthPoints(self) -> float:
        return (
            self.getMaxHealthPoints()
            + self.getStatTotalValue(StatIds.CUR_LIFE)
            + self.getStatTotalValue(StatIds.CUR_PERMANENT_DAMAGE)
        )

    def getMaxHealthPoints(self) -> float:
        vitalityStat: Stat = self.getStat(StatIds.VITALITY)
        effectiveVitality: float = 0
        if isinstance(vitalityStat, DetailedStat):
            detailedVitalityStat = vitalityStat
            effectiveVitality = (
                max(
                    0,
                    detailedVitalityStat.baseValue
                    + detailedVitalityStat.objectsAndMountBonusValue
                    + detailedVitalityStat.additionalValue
                    + detailedVitalityStat.alignGiftBonusValue,
                )
                + detailedVitalityStat.contextModifValue
            )
        elif isinstance(vitalityStat, Stat):
            effectiveVitality = vitalityStat.totalValue
        return (
            self.getStatTotalValue(StatIds.LIFE_POINTS)
            + effectiveVitality
            - self.getStatTotalValue(StatIds.CUR_PERMANENT_DAMAGE)
        )
