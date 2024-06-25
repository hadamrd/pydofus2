from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStats import EntityStats
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.Stat import Stat
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.abstract.AbstractStatContextualStep import (
    AbstractStatContextualStep,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.network.enums.GameContextEnum import GameContextEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.damageCalculation.tools.StatIds import StatIds


class FightShieldPointsVariationStep(AbstractStatContextualStep, IFightStep):

    COLOR: int = 10053324

    BLOCKING: bool = False

    _intValue: int

    _elementId: int

    _entityStats: EntityStats = None

    _newShieldStat: Stat = None

    _fighterInfo: GameFightFighterInformations = None

    _target: AnimatedCharacter = None

    def __init__(self, entityId: float, value: int, elementId: int):
        super().__init__(self.COLOR, str(value), entityId, GameContextEnum.FIGHT, self.BLOCKING)
        self._intValue = value
        self._elementId = elementId
        self._virtual = False
        self._entityStats = StatsManager().getStats(self._targetId)
        if self._entityStats is not None:
            self._newShieldStat = self._entityStats.getStat(StatIds.SHIELD)

    @property
    def stepType(self) -> str:
        return "shieldPointsVariation"

    @property
    def value(self) -> int:
        return self._intValue

    @property
    def virtual(self) -> bool:
        return self._virtual

    @virtual.setter
    def virtual(self, pValue: bool) -> None:
        self._virtual = pValue

    def start(self) -> None:
        self._target = DofusEntities().getEntity(self._targetId)
        self._fighterInfo = Kernel().fightEntitiesFrame.getEntityInfos(self._targetId)
        if not self._fighterInfo:
            super().executeCallbacks()
            return
        self.apply()

    def apply(self) -> None:
        super().start()

    def onAnimationEnd(self, pEvent) -> None:
        self.start()
