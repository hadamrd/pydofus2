from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.types.Selection import Selection
from pydofus2.com.ankamagames.atouin.utils.CellUtil import CellUtil
from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import EntitiesManager
from pydofus2.com.ankamagames.atouin.types.GraphicCell import GraphicCell
from pydofus2.com.ankamagames.atouin.messages.AdjacentMapClickMessage import (
    AdjacentMapClickMessage,
)
from pydofus2.com.ankamagames.atouin.messages.CellClickMessage import CellClickMessage
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import SpellLevel
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStats import EntityStats
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightTurnFrame import FightTurnFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
    CurrentPlayedFighterManager,
)
from pydofus2.com.ankamagames.dofus.network.enums.GameActionFightInvisibilityStateEnum import (
    GameActionFightInvisibilityStateEnum,
)
from pydofus2.com.ankamagames.dofus.network.enums.GameActionMarkTypeEnum import GameActionMarkTypeEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightCastOnTargetRequestMessage import (
    GameActionFightCastOnTargetRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightCastRequestMessage import (
    GameActionFightCastRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.dofus.types.entities.Glyph import Glyph
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.entities.messages.EntityClickMessage import (
    EntityClickMessage,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.map.LosDetector import LosDetector
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.Cross import Cross
from pydofus2.com.ankamagames.jerakine.types.zones.Custom import Custom
from pydofus2.com.ankamagames.jerakine.types.zones.Lozenge import Lozenge
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import (
    SpellShapeEnum,
)
from pydofus2.damageCalculation.tools.StatIds import StatIds

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightBattleFrame import (
        FightBattleFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import (
        FightContextFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
        FightEntitiesFrame,
    )

logger = Logger("Dofus2")


class FightSpellCastFrame(Frame):

    SELECTION_RANGE: str = "SpellCastRange"

    SELECTION_PORTALS: str = "SpellCastPortals"

    SELECTION_LOS: str = "SpellCastLos"

    SELECTION_TARGET: str = "SpellCastTarget"

    SELECTION_CENTER_TARGET: str = "SELECTION_CENTER_TARGET"

    FORBIDDEN_CURSOR_NAME: str = "SpellCastForbiddenCusror"

    MAX_TOOLTIP: int = 10

    _currentTargetIsTargetable: bool

    _spellLevel: object

    _spellId: int

    _portalsSelection: Selection

    _targetSelection: Selection

    _targetCenterSelection: Selection

    _currentCell: int = -1

    _cancelTimer: BenchmarkTimer

    _lastTargetStatus: bool = True

    _isInfiniteTarget: bool

    _targetingThroughPortal: bool

    _clearTargetTimer: BenchmarkTimer

    _spellmaximumRange: int

    _currentCellEntity: AnimatedCharacter

    _fightContextFrame: "FightContextFrame"

    def __init__(self, spellId: int):
        super().__init__()
        self._spellId = spellId
        self._cancelTimer = BenchmarkTimer(0.05, self.cancelCast)
        if spellId or not PlayedCharacterManager().currentWeapon:
            for i in PlayedCharacterManager().spellsInventory:
                if i.spellId == self._spellId:
                    self._spellLevel = i.spellLevel
        else:
            weapon = PlayedCharacterManager().currentWeapon
            self._spellLevel = {
                "effects": weapon.effects,
                "castTestLos": weapon.castTestLos,
                "castInLine": weapon.castInLine,
                "castInDiagonal": weapon.castInDiagonal,
                "minRange": weapon.minRange,
                "range": weapon.range,
                "apCost": weapon.apCost,
                "needFreeCell": False,
                "needTakenCell": False,
                "needFreeTrapCell": False,
                "name": weapon.name,
                "playerId": PlayedCharacterManager().id,
            }
        self._clearTargetTimer = BenchmarkTimer(0.05, self.onClearTarget)

    def isCurrentTargetTargetable(self) -> bool:
        return self._currentTargetIsTargetable

    @classmethod
    def updateRangeAndTarget(cls) -> None:
        castFrame: "FightSpellCastFrame" = Kernel().worker.getFrame("FightSpellCastFrame")
        if castFrame:
            castFrame.removeRange()
            castFrame.drawRange()
            castFrame.refreshTarget(True)

    @property
    def priority(self) -> int:
        return Priority.HIGHEST

    @property
    def spellId(self) -> int:
        return self._spellId

    def pushed(self) -> bool:
        self._fightContextFrame = Kernel().worker.getFrame("FightContextFrame")
        fef: "FightEntitiesFrame" = Kernel().worker.getFrame("FightEntitiesFrame")
        fighters = fef.entities
        for actorInfos in fighters:
            fighterInfos = actorInfos
            character = DofusEntities.getEntity(fighterInfos.contextualId)
            if (
                character
                and fighterInfos.contextualId != CurrentPlayedFighterManager().currentFighterId
                and fighterInfos.stats.invisibilityState == GameActionFightInvisibilityStateEnum.DETECTED
            ):
                character.canSeeThrough = True
                character.canWalkThrough = False
                character.canWalkTo = False
        self._cancelTimer.reset()
        self._lastTargetStatus = True
        if self._spellId == 0:
            if PlayedCharacterManager().currentWeapon:
                self._usedWrapper = PlayedCharacterManager().currentWeapon
            else:
                self._usedWrapper = SpellWrapper.create(0, 1, False, PlayedCharacterManager().id)
        else:
            self._usedWrapper = SpellWrapper.getSpellWrapperById(
                self._spellId, CurrentPlayedFighterManager().currentFighterId
            )
        self.drawRange()
        self.refreshTarget()
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, CellOverMessage):
            conmsg = msg
            FightContextFrame.currentCell = conmsg.cellId
            self.refreshTarget()
            return False

        elif isinstance(msg, EntityMouseOutMessage):
            self.clearTarget()
            return False

        elif isinstance(msg, CellOutMessage):
            comsg = msg
            EntitiesManager().getEntityOnCell(comsg.cellId, AnimatedCharacter)
            self.removeTeleportationPreview()
            self.removeSummoningPreview()
            self.clearTarget()
            return False

        elif isinstance(msg, EntityMouseOverMessage):
            emomsg = msg
            FightContextFrame.currentCell = emomsg.entity.position.cellId
            self.refreshTarget()
            return False

        elif isinstance(msg, TimelineEntityOverAction):
            teoa = msg
            timelineEntity = DofusEntities.getEntity(teoa.targetId)
            if timelineEntity and timelineEntity.position and timelineEntity.position.cellId > -1:
                FightContextFrame.currentCell = timelineEntity.position.cellId
                self.refreshTarget()
            return False

        if isinstance(msg, TimelineEntityOutAction):
            teouta = msg
            DofusEntities.getEntity(teouta.targetId)
            self.removeTeleportationPreview()
            self.removeSummoningPreview()
            return False

        if isinstance(msg, CellClickMessage):
            ccmsg = msg
            self.castSpell(ccmsg.cellId)
            return True

        elif isinstance(msg, EntityClickMessage):
            ecmsg = msg
            if self._fightTeleportationPreview and self._fightTeleportationPreview.isPreview(ecmsg.entity.id):
                self.castSpell(ecmsg.entity.position.cellId)
            else:
                self.castSpell(ecmsg.entity.position.cellId, ecmsg.entity.id)
            return True

        elif isinstance(msg, TimelineEntityClickAction):
            teica = msg
            self.castSpell(0, teica.fighterId, True)
            return True

        elif isinstance(msg, (AdjacentMapClickMessage, MouseRightClickMessage)):
            self.cancelCast()
            return True

        elif isinstance(msg, BannerEmptySlotClickAction):
            self.cancelCast()
            return True

        elif isinstance(msg, MouseClickMessage):
            if KeyPoll().isDown(Keyboard.ALTERNATE) and not (
                isinstance(msg.target, GraphicCell) and self.isValidCell(msg.target.cellId)
            ):
                self.cancelCast()
                self._cancelTimer.start()
            return False

        else:
            return False

    def pulled(self) -> bool:
        fbf: "FightBattleFrame" = Kernel().worker.getFrame("FightBattleFrame")
        if fbf:
            fef: "FightEntitiesFrame" = Kernel().worker.getFrame("FightEntitiesFrame")
            fighters = fef.entities
            for actorInfos in fighters:
                fighterInfos = actorInfos
                character = DofusEntities.getEntity(actorInfos.contextualId)
                if (
                    character
                    and actorInfos.contextualId != CurrentPlayedFighterManager().currentFighterId
                    and fighterInfos.stats.invisibilityState == GameActionFightInvisibilityStateEnum.VISIBLE
                ):
                    character.canSeeThrough = False
                    character.canWalkThrough = False
                    character.canWalkTo = False
        self._clearTargetTimer.cancel()
        self._cancelTimer.cancel()
        self.removeRange()
        self.removeTarget()
        self.removeSummoningPreview()
        self.removeTeleportationPreview(True)
        return True

    def entityMovement(self, pEntityId: float) -> None:
        if self._currentCellEntity and self._currentCellEntity.id == pEntityId:
            self.removeSummoningPreview()
            if self._fightTeleportationPreview:
                self.removeTeleportationPreview()
        elif self._fightTeleportationPreview and pEntityId in self._fightTeleportationPreview.getEntitiesIds():
            self.removeTeleportationPreview()

    def refreshTarget(self, force: bool = False) -> None:
        updateStrata: bool = False
        if self._clearTargetTimer.running:
            self._clearTargetTimer.reset()
        target: int = FightContextFrame.currentCell
        if target == -1:
            return
        self._targetingThroughPortal = False
        newTarget: int = -1
        if (
            SelectionManager().isInside(target, self.SELECTION_PORTALS)
            and SelectionManager().isInside(target, self.SELECTION_LOS)
            and self._spellId != 0
        ):
            newTarget = self.getTargetThroughPortal(target, True)
            if newTarget != target:
                self._targetingThroughPortal = True
                target = newTarget
        self.removeSummoningPreview()
        self.removeTeleportationPreview()
        if not force and (self._currentCell == target and self._currentCell != newTarget):
            if self._targetSelection and self.isValidCell(target):
                self.showTargetsTooltips()
            return
        self._currentCell = target
        entitiesOnCell: list = EntitiesManager().getEntitiesOnCell(self._currentCell, AnimatedCharacter)
        self._currentCellEntity = self.getParentEntity(entitiesOnCell[0]) if len(entitiesOnCell) > 0 else None
        fightTurnFrame: "FightTurnFrame" = Kernel().worker.getFrame("FightTurnFrame")
        if not fightTurnFrame:
            return
        myTurn: bool = fightTurnFrame.myTurn
        _currentTargetIsTargetable = self.isValidCell(target)
        if _currentTargetIsTargetable:
            if not self._targetSelection:
                self._targetSelection = Selection()
                self._targetCenterSelection = Selection()
                ignoreMaxSize = True
                spellShape = self.getSpellShape()
                if spellShape == SpellShapeEnum.l:
                    ignoreMaxSize = False
                self._targetCenterSelection.zone = Cross(0, 0, DataMapProvider())
                SelectionManager().addSelection(self._targetCenterSelection, self.SELECTION_CENTER_TARGET)
                SelectionManager().addSelection(self._targetSelection, self.SELECTION_TARGET)
            if not self._targetSelection.zone or self._targetSelection.zone is Custom:
                entityInfo = FightEntitiesFrame.getCurrentInstance().getEntityInfos(self._spellLevel["playerId"])
                if entityInfo:
                    cellId = entityInfo.disposition.cellId
                    spellZone = SpellZoneManager().getSpellZone(self._spellLevel, True, ignoreMaxSize, target, cellId)
                    self._spellmaximumRange = spellZone.radius
                    self._targetSelection.zone = spellZone
            currentFighterId = CurrentPlayedFighterManager().currentFighterId
            entityInfos = FightEntitiesFrame.getCurrentInstance().getEntityInfos(currentFighterId)
            if entityInfos:
                if self._targetingThroughPortal:
                    self._targetSelection.zone.direction = MapPoint(
                        MapPoint.fromCellId(entityInfos.disposition.cellId)
                    ).advancedOrientationTo(MapPoint.fromCellId(FightContextFrame.currentCell), False)
                else:
                    self._targetSelection.zone.direction = MapPoint(
                        MapPoint.fromCellId(entityInfos.disposition.cellId)
                    ).advancedOrientationTo(MapPoint.fromCellId(target), False)
            renderer = self._targetSelection.renderer
            if Atouin().options.getOption("transparentOverlayMode") and self._spellmaximumRange != 63:
                renderer.currentStrata = PlacementStrataEnums.STRATA_NO_Z_ORDER
                SelectionManager().update(SELECTION_TARGET, target, True)
                SelectionManager().update(SELECTION_CENTER_TARGET, target, True)
            else:
                if renderer.currentStrata == PlacementStrataEnums.STRATA_NO_Z_ORDER:
                    renderer.currentStrata = PlacementStrataEnums.STRATA_AREA
                    updateStrata = True
                SelectionManager().update(SELECTION_TARGET, target, updateStrata)
                SelectionManager().update(SELECTION_CENTER_TARGET, target, updateStrata)
            if myTurn:
                LinkedCursorSpriteManager().removeItem(FORBIDDEN_CURSOR_NAME)
                self._lastTargetStatus = True
            else:
                if self._lastTargetStatus:
                    LinkedCursorSpriteManager().addItem(FORBIDDEN_CURSOR_NAME, self._cursorData, True)
                self._lastTargetStatus = False
            self.showTargetsTooltips()
        else:
            if self._lastTargetStatus:
                LinkedCursorSpriteManager().addItem(FORBIDDEN_CURSOR_NAME, self._cursorData, True)
            self.removeTarget()
            self._lastTargetStatus = False
            self.hideTargetsTooltips()

    def isTeleportationPreviewEntity(self, pEntityId: float) -> bool:
        return self._fightTeleportationPreview and self._fightTeleportationPreview.isPreview(pEntityId)

    def isSummoningPreviewEntity(self, pEntityId: float) -> bool:
        return self._summoningPreview and self._summoningPreview.isPreview(pEntityId)

    def getSummonPreview(self, pEntityId: float) -> AnimatedCharacter:
        if self._summoningPreview:
            return self._summoningPreview.getSummonPreview(pEntityId)
        return None

    def drawRange(self) -> None:
        if self._spellLevel == None:
            return
        currentFighterId: float = CurrentPlayedFighterManager().currentFighterId
        entityInfos: GameFightFighterInformations = FightEntitiesFrame.getCurrentInstance().getEntityInfos(
            currentFighterId
        )
        origin: int = entityInfos.disposition.cellId
        playerStats: EntityStats = CurrentPlayedFighterManager().getStats()
        range: int = self._spellLevel["range"]
        minRange: int = self._spellLevel["minRange"]
        spellShape: int = self.getSpellShape()
        castInLine: bool = self._spellLevel["castInLine"] or spellShape == SpellShapeEnum.l
        mpWithPortals: list[MapPoint] = MarkedCellsManager().getMarksMapPoint(GameActionMarkTypeEnum.PORTAL)
        if (
            not castInLine
            and not self._spellLevel["castInDiagonal"]
            and not self._spellLevel["castTestLos"]
            and range == 63
        ):
            self._isInfiniteTarget = True
            if mpWithPortals == None or len(mpWithPortals) < 2:
                return
        else:
            self._isInfiniteTarget = False
        if self._spellLevel["rangeCanBeBoosted"]:
            range += playerStats.getStatTotalValue(StatIds.RANGE) - playerStats.getStatAdditionalValue(StatIds.RANGE)
        if range < minRange:
            range = minRange
        range = min(range, AtouinConstants.MAP_WIDTH * AtouinConstants.MAP_HEIGHT)
        if range < 0:
            range = 0
        rangeSelection: Selection = Selection()
        if castInLine and self._spellLevel["castInDiagonal"]:
            shapePlus = Cross(minRange, range, DataMapProvider())
            shapePlus.allDirections = True
            rangeSelection.zone = shapePlus
        elif castInLine:
            rangeSelection.zone = Cross(minRange, range, DataMapProvider())
        elif self._spellLevel["castInDiagonal"]:
            shapePlus = Cross(minRange, range, DataMapProvider())
            shapePlus.diagonal = True
            rangeSelection.zone = shapePlus
        else:
            rangeSelection.zone = Lozenge(minRange, range, DataMapProvider())
        untargetableCells: list[int] = list[int]()
        losSelection: Selection = Selection()
        allCells: list[int] = rangeSelection.zone.getCells(origin)
        if not self._spellLevel["castTestLos"]:
            losSelection.zone = Custom(allCells)
        else:
            losSelection.zone = Custom(LosDetector.getCell(DataMapProvider(), allCells, MapPoint.fromCellId(origin)))
            noLosRangeCell = rangeSelection.zone.getCells(origin)
            losRangeCell = losSelection.zone.getCells(origin)
            num = len(noLosRangeCell)
            for i in range(num):
                cellId = noLosRangeCell[i]
                if cellId not in losRangeCell:
                    untargetableCells.append(cellId)
        portalUsableCells: list[int] = list[int]()
        cells: list[int] = list[int]()
        if mpWithPortals and len(mpWithPortals) >= 2:
            for c in losSelection.zone.getCells(origin):
                cAfterPortal = self.getTargetThroughPortal(c)
                if cAfterPortal != c:
                    self._targetingThroughPortal = True
                    if self.isValidCell(cAfterPortal, True):
                        if self._spellLevel["castTestLos"]:
                            entryMarkPortal = MarkedCellsManager().getMarkAtCellId(c, GameActionMarkTypeEnum.PORTAL)
                            teamPortals = MarkedCellsManager().getMarksMapPoint(
                                GameActionMarkTypeEnum.PORTAL, entryMarkPortal.teamId
                            )
                            portalsCellIds = LinkedCellsManager().getLinks(MapPoint.fromCellId(c), teamPortals)
                            exitPortal = portalsCellIds.pop()
                            lastPortalMp = MapPoint.fromCellId(exitPortal)
                            newTargetMp = MapPoint.fromCellId(cAfterPortal)
                            cellsFromLine = Dofus2Line.getLine(lastPortalMp.cellId, newTargetMp.cellId)
                            for cellFromLine in cellsFromLine:
                                mp = MapPoint.fromCoords(cellFromLine.x, cellFromLine.y)
                                cells.append(mp.cellId)
                            cellsWithLosOk = LosDetector.getCell(DataMapProvider(), cells, lastPortalMp)
                            if cAfterPortal in cellsWithLosOk:
                                portalUsableCells.append(c)
                            else:
                                untargetableCells.append(c)
                        else:
                            portalUsableCells.append(c)
                    else:
                        untargetableCells.append(c)
                    self._targetingThroughPortal = False
        losCells: list[int] = list[int]()
        losSelectionCells: list[int] = losSelection.zone.getCells(origin)
        for selectionCellId in losSelectionCells:
            if portalUsableCells.find(selectionCellId) != -1:
                losCells.append(selectionCellId)
            elif (
                self._usedWrapper is SpellWrapper
                and self._usedWrapper.spellLevelInfos
                and (
                    self._usedWrapper.spellLevelInfos.needFreeCell
                    and self.cellHasEntity(selectionCellId)
                    or self._usedWrapper.spellLevelInfos.needFreeTrapCell
                    and MarkedCellsManager().cellHasTrap(selectionCellId)
                )
            ):
                untargetableCells.append(selectionCellId)
            elif untargetableCells.find(selectionCellId) == -1:
                losCells.append(selectionCellId)
        losSelection.zone = Custom(losCells)
        SelectionManager().addSelection(losSelection, self.SELECTION_LOS, origin)
        if len(untargetableCells) > 0:
            rangeSelection.zone = Custom(untargetableCells)
            SelectionManager().addSelection(rangeSelection, self.SELECTION_RANGE, origin)
        else:
            rangeSelection.zone = Custom(list[int]())
            SelectionManager().addSelection(rangeSelection, self.SELECTION_RANGE, origin)
        if len(portalUsableCells) > 0:
            self._portalsSelection = Selection()
            self._portalsSelection.zone = Custom(portalUsableCells)
            SelectionManager().addSelection(self._portalsSelection, self.SELECTION_PORTALS, origin)

    def removeTeleportationPreview(self, destroy: bool = False) -> None:
        if self._fightTeleportationPreview:
            self._fightTeleportationPreview.remove(destroy)
            if destroy:
                self._fightTeleportationPreview = None

    def removeSummoningPreview(self) -> None:
        if self._summoningPreview:
            self._summoningPreview.remove()

    def clearTarget(self) -> None:
        if not self._clearTargetTimer.running:
            self._clearTargetTimer.start()

    def onClearTarget(self, event) -> None:
        self.refreshTarget()

    def getTargetThroughPortal(self, target: int, drawLinks: bool = False) -> int:
        if self._spellLevel and self._spellLevel["effects"]:
            for effect in self._spellLevel["effects"]:
                if effect.effectId == ActionIds.ACTION_FIGHT_DISABLE_PORTAL:
                    return target
        currentFighterId: float = CurrentPlayedFighterManager().currentFighterId
        entityInfos: GameFightFighterInformations = FightEntitiesFrame.getCurrentInstance().getEntityInfos(
            currentFighterId
        )
        if not entityInfos:
            return target
        markedCellsManager: MarkedCellsManager = MarkedCellsManager()
        mpWithPortals: list[MapPoint] = markedCellsManager.getMarksMapPoint(GameActionMarkTypeEnum.PORTAL)
        if not mpWithPortals or len(mpWithPortals) < 2:
            return target
        for portalp in mpWithPortals:
            portalMark = markedCellsManager.getMarkAtCellId(portalp.cellId, GameActionMarkTypeEnum.PORTAL)
            if portalMark and portalMark.active:
                if portalp.cellId == target:
                    targetPortal = portalp
        if not targetPortal:
            return target
        mpWithPortals = markedCellsManager.getMarksMapPoint(GameActionMarkTypeEnum.PORTAL, portalMark.teamId)
        portalsCellIds: list[int] = LinkedCellsManager().getLinks(targetPortal, mpWithPortals)
        exitPoint: MapPoint = MapPoint.fromCellId(portalsCellIds.pop())
        fighterPoint: MapPoint = MapPoint.fromCellId(entityInfos.disposition.cellId)
        if not fighterPoint:
            return target
        symmetricalTargetX: int = targetPortal.x - fighterPoint.x + exitPoint.x
        symmetricalTargetY: int = targetPortal.y - fighterPoint.y + exitPoint.y
        if not MapPoint.isInMap(symmetricalTargetX, symmetricalTargetY):
            return AtouinConstants.MAP_CELLS_COUNT + 1
        newTargetPoint = MapPoint.fromCoords(symmetricalTargetX, symmetricalTargetY)
        if drawLinks:
            entryVector = list[int]()
            entryVector.append(fighterPoint.cellId)
            entryVector.append(targetPortal.cellId)
            if newTargetPoint.cellId < AtouinConstants.MAP_CELLS_COUNT:
                exitVector = list[int]()
                exitVector.append(exitPoint.cellId)
                exitVector.append(newTargetPoint.cellId)
        return newTargetPoint.cellId

    def checkSpellCostAndPlayerAp(self) -> int:
        spell: SpellWrapper = None
        for spell in PlayedCharacterManager().spellsInventory:
            if spell.spellId == self._spellLevel["spellId"] and spell.apCost != self._spellLevel["apCost"]:
                self._spellLevel["apCost"] = spell.apCost
        return CurrentPlayedFighterManager().getStats().getStatTotalValue(StatIds.ACTION_POINTS)

    def castSpell(self, cell: int, targetId: float = 0, forceCheckForRange: bool = False) -> None:
        fightTurnFrame: "FightTurnFrame" = Kernel().worker.getFrame("FightTurnFrame")
        if not fightTurnFrame:
            return
        apCurrent: int = self.checkSpellCostAndPlayerAp()
        if apCurrent < self._spellLevel["apCost"]:
            return
        if forceCheckForRange and self._spellLevel["maximalRange"] < 63:
            if cell == 0 and targetId != 0:
                entity = DofusEntities.getEntity(targetId)
                if entity and entity.position:
                    cell = entity.position.cellId
            if SelectionManager().isInside(cell, self.SELECTION_RANGE) or not SelectionManager().isInside(
                cell, self.SELECTION_LOS
            ):
                return
        if not fightTurnFrame.myTurn:
            return
        fightBattleFrame: FightBattleFrame = Kernel().worker.getFrame(FightBattleFrame)
        if fightBattleFrame and fightBattleFrame.fightIsPaused:
            self.cancelCast()
            return
        if (
            targetId != 0
            and not FightEntitiesFrame.getCurrentInstance().entityIsIllusion(targetId)
            and not (self._fightTeleportationPreview and self._fightTeleportationPreview.isPreview(targetId))
            and CurrentPlayedFighterManager().canCastThisSpell(self._spellId, self._spellLevel["spellLevel"], targetId)
        ):
            gafcotrmsg = GameActionFightCastOnTargetRequestMessage()
            gafcotrmsg.init(self._spellId, targetId)
            ConnectionsHandler()._conn.send(gafcotrmsg)
        elif self.isValidCell(cell):
            self.removeSummoningPreview()
            self.removeTeleportationPreview(True)
            gafcrmsg = GameActionFightCastRequestMessage()
            gafcrmsg.init(self._spellId, cell)
            ConnectionsHandler()._conn.send(gafcrmsg)
        self.cancelCast()

    def cancelCast(self, *args) -> None:
        self.removeSummoningPreview()
        self.removeTeleportationPreview(True)
        self._cancelTimer.cancel()
        Kernel().worker.removeFrame(self)

    def removeRange(self) -> None:
        s: Selection = SelectionManager().getSelection(self.SELECTION_RANGE)
        if s:
            s.remove()
        los: Selection = SelectionManager().getSelection(self.SELECTION_LOS)
        if los:
            los.remove()
        ps: Selection = SelectionManager().getSelection(self.SELECTION_PORTALS)
        if ps:
            ps.remove()
            self._portalsSelection = None
        self._isInfiniteTarget = False

    def removeTarget(self) -> None:
        s: Selection = SelectionManager().getSelection(self.SELECTION_TARGET)
        if s:
            s.remove()
        s = SelectionManager().getSelection(self.SELECTION_CENTER_TARGET)
        if s:
            s.remove()

    def cellHasEntity(self, cellId: int) -> bool:
        isPreviewedEntity: bool = False
        entity: IEntity = None
        entities: list = EntitiesManager().getEntitiesOnCell(cellId, AnimatedCharacter)
        if entities == None or len(entities) <= 0:
            return False
        isSummoningPreview: bool = self.hasSummoningPreview
        isTeleportationPreview = self._fightTeleportationPreview is not None
        entityId: float = None
        for entity in entities:
            entityId = entity.id
            isPreviewedEntity = False
            if isSummoningPreview:
                if self._summoningPreview.isPreview(entityId):
                    isPreviewedEntity = True
            if not isPreviewedEntity and isTeleportationPreview:
                if self._fightTeleportationPreview.isPreview(entityId):
                    isPreviewedEntity = True
            if not isPreviewedEntity:
                return True
        return False

    def isValidCell(self, cell: int, ignorePortal: bool = False) -> bool:
        spellLevel: SpellLevel = None
        entities: list = None
        entity: IEntity = None
        isGlyph = False
        valid: bool = False
        if not CellUtil.isValidCellIndex(cell):
            return False
        cellData: "Cell" = MapDisplayManager().dataMap.cells[cell]
        if not cellData or cellData.farmCell:
            return False
        if self._isInfiniteTarget:
            return True
        if self._spellId and self._spellLevel:
            spellLevel = self._spellLevel["spellLevelInfos"]
            entities = EntitiesManager().getEntitiesOnCell(cell)
            for entity in entities:
                if not (self.isTeleportationPreviewEntity(entity.id) or self.isSummoningPreviewEntity(entity.id)):
                    if not CurrentPlayedFighterManager().canCastThisSpell(
                        self._spellLevel["spellId"],
                        self._spellLevel["spellLevel"],
                        entity.id,
                    ):
                        return False
                    isGlyph = isinstance(entity, Glyph)
                    if spellLevel.needFreeTrapCell and isGlyph and entity.glyphType == GameActionMarkTypeEnum.TRAP:
                        return False
                    if self.sespellLevel["needFreeCell"] and not isGlyph:
                        return False
        if self._targetingThroughPortal and not ignorePortal:
            valid = self.isValidCell(self.getTargetThroughPortal(cell), True)
            if not valid:
                return False
        if self._targetingThroughPortal:
            if cellData.nonWalkableDuringFight:
                return False
            return cellData.mov
        return SelectionManager().isInside(cell, self.SELECTION_LOS)

    def getSpellShape(self) -> int:
        spellShape: int = 0
        spellEffect: EffectInstance = None
        for spellEffect in self._spellLevel["effects"]:
            if spellEffect.zoneShape != 0 and (
                spellEffect.zoneSize > 0
                or spellEffect.zoneSize == 0
                and (spellEffect.zoneShape == SpellShapeEnum.P or spellEffect.zoneMinSize < 0)
            ):
                spellShape = spellEffect.zoneShape
        return spellShape
