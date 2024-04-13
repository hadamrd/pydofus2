from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightVisibilityStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _visibility: bool

    def __init__(self, fighterId: float, visibility: bool):
        super().__init__()
        self._fighterId = fighterId
        self._visibility = visibility

    @property
    def stepType(self) -> str:
        return "visibility"

    def start(self) -> None:
        entity = DofusEntities().getEntity(self._fighterId)
        if entity:
            entity.visible = self._visibility
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
