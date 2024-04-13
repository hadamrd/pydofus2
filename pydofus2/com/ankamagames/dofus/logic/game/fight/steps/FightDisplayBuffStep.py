from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.BuffManager import BuffManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdProtocol import ActionIdProtocol
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.FightActionPointsVariationStep import (
    FightActionPointsVariationStep,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.FightMovementPointsVariationStep import (
    FightMovementPointsVariationStep,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import BasicBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StatBuff import StatBuff
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import ISequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencableListener import ISequencableListener


class FightDisplayBuffStep(AbstractSequencable, IFightStep, ISequencableListener):

    _buff: BasicBuff

    _virtualStep: IFightStep

    def __init__(self, buff: BasicBuff):
        super().__init__()
        self._buff = buff

    @property
    def stepType(self) -> str:
        return "displayBuff"

    def start(self) -> None:
        statName: str = None
        buffUnknown = True
        if self._buff.actionId == ActionIdProtocol.ACTION_CHARACTER_UPDATE_BOOST:
            buffUnknown = not BuffManager().updateBuff(self._buff)
        elif buffUnknown:
            if isinstance(self._buff, StatBuff):
                statName = self._buff.statName
                if statName == "movementPoints":
                    self._virtualStep = FightMovementPointsVariationStep(
                        self._buff.targetId, self._buff.delta, False, False, False
                    )
                if statName == "actionPoints":
                    self._virtualStep = FightActionPointsVariationStep(
                        self._buff.targetId, self._buff.delta, False, False, False
                    )
            BuffManager().addBuff(self._buff)
        self.executeCallbacks()

    def stepFinished(self, step: ISequencable) -> None:
        self._virtualStep.removeListener(self)
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._buff.targetId]
