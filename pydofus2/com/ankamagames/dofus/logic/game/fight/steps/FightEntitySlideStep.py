from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.fightEvents.FightEventsHelper import (
    FightEventsHelper,
)
from typing import TYPE_CHECKING
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightSpellCastFrame import (
    FightSpellCastFrame,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import (
        FightContextFrame,
    )
    from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter

from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
    FightEntitiesFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.FightEventEnum import FightEventEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

logger = Logger("Dofus2")


class FightEntitySlideStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _startCell: MapPoint

    _endCell: MapPoint

    _entity: "AnimatedCharacter"

    _fightContextFrame: "FightContextFrame"

    _ttCacheName: str

    _ttName: str

    def __init__(self, fighterId: float, startCell: MapPoint, endCell: MapPoint):
        super().__init__()
        self._fighterId = fighterId
        self._startCell = startCell
        self._endCell = endCell
        infos: "GameFightFighterInformations" = FightEntitiesFrame.getCurrentInstance().getEntityInfos(fighterId)
        infos.disposition.cellId = endCell.cellId
        self._entity: "AnimatedCharacter" = DofusEntities.getEntity(self._fighterId)
        self._fightContextFrame: "FightContextFrame" = Kernel().worker.getFrame("FightContextFrame")

    @property
    def stepType(self) -> str:
        return "entitySlide"

    def start(self) -> None:
        if self._entity:
            self._entity.direction = self._startCell.advancedOrientationTo(self._endCell)
            if not self._entity.position == self._startCell:
                logger.warn(
                    f"We were ordered to slide {self._fighterId} from {self._startCell.cellId}, but self fighter is on {self._entity.position.cellId}."
                )
            fighterInfos = FightEntitiesFrame.getCurrentInstance().getEntityInfos(self._fighterId)
            fighterInfos.disposition.cellId = self._endCell.cellId
            # TODO : Uncomment this and sleep for path dyration if the server rejects the simulated behavio
            # path = MovementPath()
            # path.start = self._entity.position
            # path.end = self._endCell
            # path.addPoint(PathElement(self._entity.position, path.start.orientationTo(path.end)))
            # path.fill()
        else:
            logger.warn("Unable to slide unexisting fighter " + self._fighterId + ".")
        self.slideFinished()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]

    def slideFinished(self) -> None:
        FightSpellCastFrame.updateRangeAndTarget()
        FightEventsHelper().sendFightEvent(
            FightEventEnum.FIGHTER_SLIDE,
            [self._fighterId],
            self._fighterId,
            self.castingSpellId,
        )
        self.executeCallbacks()
