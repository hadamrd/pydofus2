from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.MarkedCellsManager import \
    MarkedCellsManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.GameActionMarkedCell import \
    GameActionMarkedCell
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable

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
        spell = Spell.getSpellById(self._markSpellId)
        originMarkSpellLevel = spell.getSpellLevel(self._markSpellGrade)
        # glyphGfxId = MarkedCellsManager().getResolvedMarkGlyphId(self._markCasterId, self._markSpellId, self._markSpellGrade, self._markImpactCell)
        # if self._markType == GameActionMarkTypeEnum.WALL or originMarkSpellLevel.hasZoneShape(SpellShapeEnum.semicolon):
        #     if glyphGfxId != 0:
        #         for cellZone in self._cells:
        #             step = AddGlyphGfxStep(glyphGfxId,cellZone.cellId, self._markId, self._markType, self._markTeamId)
        #             step.start()
        # elif glyphGfxId != 0 and not MarkedCellsManager().getGlyph(self._markId) and self._markImpactCell != -1:
        #     step = AddGlyphGfxStep(glyphGfxId, self._markImpactCell, self._markId, self._markType, self._markTeamId)
        #     step.start()
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
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._markId]
