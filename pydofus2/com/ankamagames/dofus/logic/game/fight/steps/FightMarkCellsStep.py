from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import SpellLevel
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.fightEvents.FightEventsHelper import (
    FightEventsHelper,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightTurnFrame import FightTurnFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.MarkedCellsManager import (
    MarkedCellsManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.FightEventEnum import FightEventEnum
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.MarkInstance import MarkInstance
from pydofus2.com.ankamagames.dofus.network.enums.GameActionMarkTypeEnum import (
    GameActionMarkTypeEnum,
)
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.GameActionMarkedCell import (
    GameActionMarkedCell,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable
from pydofus2.com.ankamagames.jerakine.types.positions.PathElement import PathElement

logger = Logger("Dofus2")


class FightMarkCellsStep(AbstractSequencable, IFightStep):

    _markCasterId: float

    _markId: int

    _markType: int

    _markSpellGrade: int

    _cells: list[GameActionMarkedCell]

    _markSpellId: int

    _markTeamId: int

    _markImpactCell: int

    _markActive: bool

    def __init__(
        self,
        markId: int,
        markType: int,
        cells: list[GameActionMarkedCell],
        markSpellId: int,
        markSpellGrade: int,
        markTeamId: int,
        markImpactCell: int,
        markCasterId: float,
        markActive: bool = True,
    ):
        super().__init__()
        self._markCasterId = markCasterId
        self._markId = markId
        self._markType = markType
        self._cells = cells
        self._markSpellId = markSpellId
        self._markSpellGrade = markSpellGrade
        self._markTeamId = markTeamId
        self._markImpactCell = markImpactCell
        self._markActive = markActive

    @property
    def stepType(self) -> str:
        return "markCells"

    def start(self) -> None:
        evt: str = None
        ftf: FightTurnFrame = None
        pe: PathElement = None
        updatePath: bool = False
        spell: Spell = Spell.getSpellById(self._markSpellId)
        originMarkSpellLevel: SpellLevel = spell.getSpellLevel(self._markSpellGrade)
        MarkedCellsManager().addMark(
            self._markCasterId,
            self._markId,
            self._markType,
            spell,
            originMarkSpellLevel,
            self._cells,
            self._markTeamId,
            self._markActive,
            self._markImpactCell,
        )
        mi: MarkInstance = MarkedCellsManager().getMarkDatas(self._markId)
        if mi:
            evt = FightEventEnum.UNKNOWN_FIGHT_EVENT
            if mi.markType == GameActionMarkTypeEnum.GLYPH:
                evt = FightEventEnum.GLYPH_APPEARED
            if mi.markType == GameActionMarkTypeEnum.TRAP:
                evt = FightEventEnum.TRAP_APPEARED
            if mi.markType == GameActionMarkTypeEnum.PORTAL:
                evt = FightEventEnum.PORTAL_APPEARED
            if mi.markType == GameActionMarkTypeEnum.RUNE:
                evt = FightEventEnum.RUNE_APPEARED
            else:
                logger.warn(f"Unknown mark type ({mi.markType}).")
            FightEventsHelper().sendFightEvent(evt, [mi.associatedSpell.id], 0, self.castingSpellId)
            ftf = Kernel().worker.getFrame("FightTurnFrame")
            if ftf and ftf.myTurn and ftf.lastPath:
                for pe in ftf.lastPath.path:
                    if pe.cellId not in mi.cells:
                        updatePath = True
                if updatePath:
                    ftf.updatePath()
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._markId]
