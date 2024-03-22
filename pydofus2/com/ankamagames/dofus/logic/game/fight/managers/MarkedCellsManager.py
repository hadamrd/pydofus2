from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.rtypes.Selection import Selection
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import \
    DataMapProvider
from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import \
    SpellLevel
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.MarkInstance import \
    MarkInstance
from pydofus2.com.ankamagames.dofus.network.enums.GameActionMarkCellsTypeEnum import \
    GameActionMarkCellsTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.GameActionMarkTypeEnum import \
    GameActionMarkTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.TeamEnum import TeamEnum
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.GameActionMarkedCell import \
    GameActionMarkedCell
from pydofus2.com.ankamagames.dofus.types.entities.Glyph import Glyph
from pydofus2.com.ankamagames.jerakine.interfaces.IDestroyable import \
    IDestroyable
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.Cross import Cross
from pydofus2.com.ankamagames.jerakine.types.zones.Custom import Custom
from pydofus2.com.ankamagames.jerakine.types.zones.Lozenge import Lozenge


class MarkedCellsManager(IDestroyable, metaclass=Singleton):

    MARK_SELECTIONS_PREFIX = "FightMark"

    _marks: dict[int, MarkInstance]

    _glyphs: dict[int, list]

    _markUid: int

    def __init__(self):
        super().__init__()
        self._marks = dict()
        self._glyphs = dict()
        self._markUid = 0

    def addMark(
        self,
        markCasterId: float,
        markId: int,
        markType: int,
        associatedSpell: Spell,
        associatedSpellLevel: SpellLevel,
        cells: list[GameActionMarkedCell],
        teamId: int = 2,
        markActive: bool = True,
        markImpactCellId: int = -1,
    ) -> None:
        if not self._marks.get(markId) or len(self._marks[markId].cells) == 0:
            mi = MarkInstance()
            mi.markCasterId = markCasterId
            mi.markId = markId
            mi.markType = markType
            mi.associatedSpell = associatedSpell
            mi.associatedSpellLevel = associatedSpellLevel
            mi.selections = list[Selection]()
            mi.cells = list[int]()
            mi.teamId = teamId
            mi.active = markActive
            if markImpactCellId != -1:
                mi.markImpactCellId = markImpactCellId
            elif cells and len(cells) and cells[0]:
                mi.markImpactCellId = cells[0].cellId
            else:
                Logger().warn("Adding a mark with unknown markImpactCellId!")
            if len(cells) > 0:
                markedCell = cells[0]
                s = Selection()
                cellsId = list[int]()
                for gamcell in cells:
                    cellsId.append(gamcell.cellId)
                if markedCell.cellsType == GameActionMarkCellsTypeEnum.CELLS_CROSS:
                    s.zone = Cross(0, markedCell.zoneSize, DataMapProvider())
                elif markedCell.zoneSize > 0:
                    s.zone = Lozenge(0, markedCell.zoneSize, DataMapProvider())
                else:
                    s.zone = Custom(cellsId)
                for cell in s.zone.getCells():
                    mi.cells.append(cell)
                    if mi.markType == GameActionMarkTypeEnum.TRAP:
                        DataMapProvider().obstaclesCells.append(cell)
                mi.selections.append(s)
            self._marks[markId] = mi
            self.updateDataMapProvider()

    def getMarks(self, pMarkType: int, pTeamId: int, pActiveOnly: bool = True) -> list[MarkInstance]:
        marks = list[MarkInstance]()
        for mi in self._marks:
            if (
                (pMarkType == 0 or mi.markType == pMarkType)
                and (pTeamId == TeamEnum.TEAM_SPCTEATOR or mi.teamId == pTeamId)
                and (not pActiveOnly or mi.active)
            ):
                marks.append(mi)
        return marks

    def getAllMarks(self) -> dict:
        return self._marks

    def getMarkDatas(self, markId: int) -> MarkInstance:
        return self._marks.get(markId)

    def removeMark(self, markId: int) -> None:
        cell: int = 0
        cellIndex: int = 0
        selections: list[Selection] = self._marks[markId].selections
        for s in selections:
            s.remove()
            if self._marks[markId].markType == GameActionMarkTypeEnum.TRAP:
                for cell in s.cells:
                    cellIndex = DataMapProvider().obstaclesCells.index(cell)
                    if cellIndex != -1:
                        del DataMapProvider().obstaclesCells[cellIndex]
        del self._marks[markId]
        self.updateDataMapProvider()

    def addGlyph(self, glyph: Glyph, markId: int) -> None:
        glyphList: list[Glyph] = None
        currentGlyph = self._glyphs[markId]
        if currentGlyph:
            if isinstance(currentGlyph, Glyph):
                glyphList = list[Glyph]([self._glyphs[markId], glyph])
                self._glyphs[markId] = glyphList
            elif isinstance(currentGlyph, list):
                self._glyphs[markId].append(glyph)
        else:
            self._glyphs[markId] = glyph

    def getGlyph(self, markId: int) -> Glyph:
        if isinstance(self._glyphs[markId], list):
            if len(self._glyphs[markId]):
                return self._glyphs[markId][0]
            return None
        return self._glyphs[markId]

    def removeGlyph(self, markId: int) -> None:
        if self._glyphs.get(markId):
            if isinstance(self._glyphs[markId], list):
                self._glyphs[markId].clear()
            del self._glyphs[markId]

    def getMarksMapPoint(self, markType: int, teamId: int = 2, activeOnly: bool = True) -> list[MapPoint]:
        mapPoints: list[MapPoint] = list[MapPoint]()
        for mi in self._marks.values():
            if (
                mi.markType == markType
                and (teamId == TeamEnum.TEAM_SPECTATOR or mi.teamId == teamId)
                and (not activeOnly or mi.active)
            ):
                mapPoints.append(MapPoint.fromCellId(mi.cells[0]))
        return mapPoints

    def getMarkAtCellId(self, cellId: int, markType: int = -1) -> MarkInstance:
        for mark in self._marks.values():
            if mark.markImpactCellId == cellId and (markType == -1 or markType == mark.markType):
                return mark
        return None

    def cellHasTrap(self, cellId: int) -> bool:
        for mark in self._marks.values():
            if mark.markImpactCellId == cellId and mark.markType == GameActionMarkTypeEnum.TRAP:
                return True
        return False

    def getCellIdsFromMarkIds(self, markIds: list[int]) -> list[int]:
        cellIds: list[int] = list[int]()
        for markId in markIds:
            if self._marks[markId] and self._marks[markId].cells and len(self._marks[markId].cells) == 1:
                cellIds.append(self._marks[markId].cells[0])
            else:
                Logger().warn("Can't find cellId for markId " + markId + " in getCellIdsFromMarkIds()")
        return cellIds

    def getMapPointsFromMarkIds(self, markIds: list[int]) -> list[MapPoint]:
        mapPoints: list[MapPoint] = list[MapPoint]()
        for markId in markIds:
            if self._marks[markId] and self._marks[markId].cells and len(self._marks[markId].cells) == 1:
                mapPoints.append(MapPoint.fromCellId(self._marks[markId].cells[0]))
            else:
                Logger().warn("Can't find cellId for markId " + markId + " in getMapPointsFromMarkIds()")
        return mapPoints

    def getActivePortalsCount(self, teamId: int = 2) -> int:
        count: int = 0
        for mi in self._marks.values():
            if (
                mi.markType == GameActionMarkTypeEnum.PORTAL
                and (teamId == TeamEnum.TEAM_SPECTATOR or mi.teamId == teamId)
                and mi.active
            ):
                count += 1
        return count

    def destroy(self) -> None:
        bufferId: list = list()
        for mark in self._marks:
            bufferId.append(int(mark))
        num = len(bufferId)
        for i in range(num):
            self.removeMark(bufferId[i])
        bufferId.clear()
        for glyph in self._glyphs:
            bufferId.append(int(glyph))
        num = len(bufferId)
        for i in range(num):
            self.removeGlyph(bufferId[i])
        self = None

    def onPropertyChanged(self, pEvent) -> None:
        pass

    def getSelectionUid(self) -> str:
        self._markUid += 1
        return self.MARK_SELECTIONS_PREFIX + self._markUid

    def updateDataMapProvider(self) -> None:
        markedCells: list = [None] * AtouinConstants.MAP_CELLS_COUNT
        for mi in self._marks.values():
            for cell in mi.cells:
                markedCells[cell] = mi.markType
        dmp = DataMapProvider()
        for i in range(AtouinConstants.MAP_CELLS_COUNT):
            mp = MapPoint.fromCellId(i)
            dmp.setSpecialEffects(i, (dmp.pointSpecialEffects(mp.x, mp.y) | 3) ^ 3)
            if markedCells[i]:
                dmp.setSpecialEffects(i, dmp.pointSpecialEffects(mp.x, mp.y) | markedCells[i])
        self.updateMarksNumber(GameActionMarkTypeEnum.PORTAL)

    def updateMarksNumber(self, marktype: int) -> None:
        markInstanceToNumber: list = list[list[MarkInstance]]()
        teamIds: list = list()
        for mi in self._marks.values():
            if mi.markType == marktype:
                if not markInstanceToNumber[mi.teamId]:
                    markInstanceToNumber[mi.teamId] = list()
                    teamIds.append(mi.teamId)
                markInstanceToNumber[mi.teamId].append(mi)
        for teamId in teamIds:
            markInstanceToNumber[teamId].sort(key=lambda e: e.markId)
            num = 1
            for mitn in markInstanceToNumber[teamId]:
                if self._glyphs[mitn.markId]:
                    if isinstance(self._glyphs[mitn.markId], Glyph):
                        Glyph(self._glyphs[mitn.markId]).addNumber(num)
                num += 1

    def addSelection(self, s: Selection, name: str, cellId: int = 561.0) -> None:
        if self._aSelection.get(name):
            Selection(self._aSelection[name]).remove()
        self._aSelection[name] = s
        if cellId != AtouinConstants.MAP_CELLS_COUNT + 1:
            self.update(name, cellId)
