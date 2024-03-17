from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.BuffManager import \
    BuffManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.FightEnteringStateStep import \
    FightEnteringStateStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.FightLeavingStateStep import \
    FightLeavingStateStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import \
    BasicBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StateBuff import \
    StateBuff
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencable import \
    ISequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencableListener import \
    ISequencableListener


class FightDispellEffectStep(AbstractSequencable, IFightStep, ISequencableListener):

    _fighterId: float = None

    _boostUID: int = None

    _virtualStep: IFightStep = None

    def __init__(self, fighterId: float, boostUID: int):
        super().__init__()
        self._fighterId = fighterId
        self._boostUID = boostUID

    @property
    def stepType(self) -> str:
        return "dispellEffect"

    def start(self) -> None:
        sb: StateBuff = None
        buff: BasicBuff = BuffManager().getBuff(self._boostUID, self._fighterId)
        if buff and buff is StateBuff:
            sb = buff
            if sb.actionId == ActionIds.ACTION_FIGHT_DISABLE_STATE:
                self._virtualStep = FightEnteringStateStep(sb.targetId, sb.stateId, sb.effect.durationString, buff)
            else:
                self._virtualStep = FightLeavingStateStep(sb.targetId, sb.stateId, buff)
        BuffManager().dispellUniqueBuff(self._fighterId, self._boostUID, True, False, True)
        if not self._virtualStep:
            self.executeCallbacks()
        else:
            self._virtualStep.addListener(self)
            self._virtualStep.start()

    def stepFinished(self, step: ISequencable) -> None:
        self._virtualStep.removeListener(self)
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
