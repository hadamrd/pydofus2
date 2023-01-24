from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightTurnFrame import FightTurnFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.MarkedCellsManager import (
    MarkedCellsManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.MarkInstance import MarkInstance
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightMarkActivateStep(AbstractSequencable, IFightStep):

    _markId: int

    _activate: bool

    def __init__(self, markId: int, activate: bool):
        super().__init__()
        self._markId = markId
        self._activate = activate

    @property
    def stepType(self) -> str:
        return "markActivate"

    def start(self) -> None:
        mark: MarkInstance = MarkedCellsManager().getMarkDatas(self._markId)
        if mark:
            mark.active = self._activate
            ftf: "FightTurnFrame" = Kernel().worker.getFrame("FightTurnFrame")
            if ftf and ftf.myTurn and ftf.lastPath:
                for pe in ftf.lastPath.path:
                    if pe.cellId not in mark.cells:
                        updatePath = True
                if updatePath:
                    ftf.updatePath()
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._markId]
