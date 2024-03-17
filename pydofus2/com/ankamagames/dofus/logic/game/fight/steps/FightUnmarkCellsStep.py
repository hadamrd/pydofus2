from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.MarkedCellsManager import \
    MarkedCellsManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.MarkInstance import \
    MarkInstance
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable


class FightUnmarkCellsStep(AbstractSequencable, IFightStep):

    _markId: int

    def __init__(self, markId: int):
        super().__init__()
        self._markId = markId

    @property
    def stepType(self) -> str:
        return "unmarkCells"

    def start(self) -> None:
        mi: MarkInstance = MarkedCellsManager().getMarkDatas(self._markId)
        if not mi:
            Logger().error("Trying to remove an unknown mark (" + str(self._markId) + "). Aborting.")
            self.executeCallbacks()
            return
        MarkedCellsManager().removeGlyph(self._markId)
        MarkedCellsManager().removeMark(self._markId)
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._markId]
