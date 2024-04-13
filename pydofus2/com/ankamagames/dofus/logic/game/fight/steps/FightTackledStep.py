from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import ISequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencableListener import ISequencableListener


class FightTackledStep(AbstractSequencable, IFightStep, ISequencableListener):

    _fighterId: float

    _animStep: ISequencable

    def __init__(self, fighterId: float):
        super().__init__()
        self._fighterId = fighterId

    @property
    def stepType(self) -> str:
        return "tackled"

    def start(self) -> None:
        tackledEntity: IEntity = DofusEntities().getEntity(self._fighterId)
        if not tackledEntity:
            Logger().warn("Unable to play tackle of an unexisting fighter " + str(self._fighterId) + ".")
        self.stepFinished(self)

    def stepFinished(self, step: ISequencable) -> None:
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
