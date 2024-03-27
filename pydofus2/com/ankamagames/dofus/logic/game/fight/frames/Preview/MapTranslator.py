from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import EntitiesManager
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import FightEntitiesFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.DamagePreview import DamagePreview
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.FighterTranslator import FighterTranslator
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.MarkedCellsManager import MarkedCellsManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.MarkInstance import MarkInstance
from pydofus2.com.ankamagames.dofus.network.enums.GameActionMarkTypeEnum import GameActionMarkTypeEnum
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.damageCalculation.IMapInfo import IMapInfo
from pydofus2.damageCalculation.fighterManagement.HaxeFighter import HaxeFighter
from pydofus2.damageCalculation.spellManagement.Mark import Mark
from pydofus2.mapTools import MapTools


class MapTranslator(IMapInfo):
    def __init__(self, context:FightEntitiesFrame):
        self._context = context

    @staticmethod
    def createHaxeMark(mark: MarkInstance):
        spell = None
        spellToGet = None

        if mark.markType == GameActionMarkTypeEnum.WALL:
            spellLevel = Spell.getSpellById(mark.associatedSpell.id).getSpellLevel(mark.associatedSpellLevel.grade)
            spell = DamagePreview.createHaxeSpell(spellLevel)
        elif mark.markType == GameActionMarkTypeEnum.PORTAL:
            spell = DamagePreview.createHaxeSpell(mark.associatedSpellLevel)
        else:
            for effect in mark.associatedSpellLevel.effects:
                spellToGet = Spell.getSpellById(effect.parameter0)
                if spellToGet:
                    spell = DamagePreview.createHaxeSpell(spellToGet.getSpellLevel(effect.parameter1))
                    break

        if spell is None:
            return None

        haxeMark = Mark()
        haxeMark.markId = mark.markId
        haxeMark.setMarkType(mark.markType)
        haxeMark.setAssociatedSpell(spell)
        haxeMark.mainCell = mark.markImpactCellId
        haxeMark.cells = MapTranslator.vectorToArray(mark.cells)
        haxeMark.teamId = mark.teamId
        haxeMark.active = mark.active
        haxeMark.casterId = mark.markCasterId
        return haxeMark

    @staticmethod
    def vectorToArray(vector):
        array = []
        for value in vector:
            array.append(value)
        return array

    def getEveryFighterId(self):
        fightEntities = self._context.getEntitiesIdsList()
        fighters = []
        for entityId in fightEntities:
            stats = StatsManager().getStats(entityId)
            if stats is not None and stats.getHealthPoints() > 0:
                fighters.append(entityId)
        return fighters

    def getFightersInitialPositions(self):
        fightEntities = self._context.entities
        positions = list()
        for infos in fightEntities.values():
            stats = StatsManager().getStats(infos.contextualId)
            if stats is not None and stats.getHealthPoints() > 0:
                positions.append({"id": infos.contextualId, "cell": infos.disposition.cellId})
        return positions

    def getCarriedFighterIdBy(self, carrier: HaxeFighter):
        entities = EntitiesManager().getEntitiesOnCell(carrier.getCurrentPositionCell(), AnimatedCharacter)
        for entity in entities:
            if entity.id == carrier.id and entity.carriedEntity is not None:
                carriedEntity = entity.carriedEntity
                if carriedEntity is not None:
                    return carriedEntity.id
        return HaxeFighter.INVALID_ID

    def getFighterById(self, id: float):
        infos = self._context.entitiesFrame.getEntityInfos(id)
        if infos is not None:
            return FighterTranslator(infos, id)
        return None

    def isCellWalkable(self, cell: int):
        if not MapTools.isValidCellId(cell):
            return False
        return DataMapProvider().pointMov(MapTools.getCellIdXCoord(cell), MapTools.getCellIdYCoord(cell))

    def getMarkInteractingWithCell(self, cell: int, markType: int = 0):
        marks = MarkedCellsManager().getMarks(markType, 2, True)
        returnMarks = []
        for mark in marks:
            if cell in mark.cells:
                if markType == GameActionMarkTypeEnum.NONE or markType == mark.markType:
                    returnMarks.append(self.createHaxeMark(mark))
        return returnMarks

    def getMarks(self, markType: int = 0, teamId: int = 2):
        marks = MarkedCellsManager().getMarks(markType, teamId, True)
        returnMarks = []
        for mark in marks:
            if markType == GameActionMarkTypeEnum.NONE or markType == mark.markType:
                returnMarks.append(self.createHaxeMark(mark))
        return returnMarks