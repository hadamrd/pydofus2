from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter

from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class FightEntitySlideStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _startCell: MapPoint

    _endCell: MapPoint

    _entity: "AnimatedCharacter"

    _ttCacheName: str

    _ttName: str

    def __init__(self, fighterId: float, startCell: MapPoint, endCell: MapPoint):
        super().__init__()
        self._fighterId = fighterId
        self._startCell = startCell
        self._endCell = endCell
        infos = Kernel().fightEntitiesFrame.getEntityInfos(fighterId)
        infos.disposition.cellId = endCell.cellId
        Logger().info(f"Slide fighter {fighterId} from {startCell.cellId} to {endCell.cellId}")
        self._entity: "AnimatedCharacter" = DofusEntities().getEntity(self._fighterId)
        self._fightContextFrame = Kernel().fightContextFrame

    @property
    def stepType(self) -> str:
        return "entitySlide"

    def start(self) -> None:
        if self._entity:
            self._entity.direction = self._startCell.advancedOrientationTo(self._endCell)
            if not self._entity.position.cellId == self._startCell.cellId:
                Logger().warn(
                    f"We were ordered to slide {self._fighterId} from {self._startCell.cellId} to {self._endCell.cellId}, but self fighter is on {self._entity.position.cellId}."
                )
            self._entity.position.cellId = self._endCell.cellId
        else:
            Logger().warn("Unable to slide unexisting fighter " + self._fighterId + ".")
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
