import math
from typing import List
from pydofus2.com.ankamagames.atouin.enums.PlacementStrataEnums import PlacementStrataEnums
from pydofus2.com.ankamagames.atouin.rtypes.Selection import Selection
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from pydofus2.com.ankamagames.dofus.datacenter.spells.EffectZone import EffectZone
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
    CurrentPlayedFighterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.DamageUtil import DamageUtil
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.uiApi.PlayedCharacterApi import PlayedCharacterApi
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.Cone import Cone
from pydofus2.com.ankamagames.jerakine.types.zones.Cross import Cross
from pydofus2.com.ankamagames.jerakine.types.zones.Custom import Custom
from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone
from pydofus2.com.ankamagames.jerakine.types.zones.Fork import Fork
from pydofus2.com.ankamagames.jerakine.types.zones.HalfLozenge import HalfLozenge
from pydofus2.com.ankamagames.jerakine.types.zones.Line import Line
from pydofus2.com.ankamagames.jerakine.types.zones.Lozenge import Lozenge
from pydofus2.com.ankamagames.jerakine.types.zones.Square import Square
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum
from pydofus2.flash.geom.Rectangle import Rectangle
from pydofus2.mapTools import MapTools
from pydofus2.mapTools.MapDirection import MapDirection


class SpellZoneManager(metaclass=Singleton):
    _self = None
    ZONE_COLOR = 10929860
    SELECTION_ZONE = "SpellCastZone"

    def __init__(self):
        self._targetSelection = None
        self._spellWrapper = None

    def displaySpellZone(self, casterId, targetCellId, sourceCellId, spellId, spellLevelId):
        self._spellWrapper = SpellWrapper.create(spellId, spellLevelId, False, casterId)
        if self._spellWrapper and targetCellId != -1 and sourceCellId != -1:
            self._targetSelection = Selection()
            self._targetSelection.renderer = ZoneDARenderer(PlacementStrataEnums.STRATA_AREA)
            self._targetSelection.color = SpellZoneManager.ZONE_COLOR
            self._targetSelection.zone = self.getSpellZone(self._spellWrapper, False, True, targetCellId, sourceCellId)
            self._targetSelection.zone.direction = MapPoint.fromCellId(sourceCellId).advancedOrientationTo(
                MapPoint.fromCellId(targetCellId), False
            )
            SelectionManager().addSelection(self._targetSelection, SpellZoneManager.SELECTION_ZONE)
            SelectionManager().update(SpellZoneManager.SELECTION_ZONE, targetCellId)
        else:
            self.removeSpellZone()

    def getPreferredPreviewZone(
        self,
        spell,
        isWholeMapShapeIgnored=False,
        isInfiniteSizeIgnored=True,
        isTooltipFilter=False,
        outputPortalCell=-1,
    ):
        biggestZone = None
        lastSurface = 0
        for effect in spell.effects:
            if effect.zoneShape != SpellShapeEnum.UNKNOWN and (not isTooltipFilter or effect.visibleInTooltip):
                currentZone = self.getZone(
                    effect.zoneShape,
                    int(effect.zoneSize),
                    int(effect.zoneMinSize),
                    isWholeMapShapeIgnored,
                    effect.zoneStopAtTarget,
                    not isinstance(spell, SpellWrapper),
                    spell.getEntityId(),
                    outputPortalCell,
                )
                currentSurface = currentZone.surface
                if not isInfiniteSizeIgnored or not currentZone.isInfinite:
                    if currentSurface > lastSurface:
                        biggestZone = currentZone
                        lastSurface = currentSurface
        return biggestZone

    def getSpellZone(
        self,
        spell,
        isWholeMapShapeIgnored=False,
        isInfiniteSizeIgnored=True,
        spellImpactCell=0,
        casterCell=0,
        isPreview=True,
        casterId=float("nan"),
        portalCell=-1,
    ) -> DisplayZone:
        finalZone = None
        direction = (
            portalCell
            if portalCell != MapTools.INVALID_CELL_ID
            else MapPoint.fromCellId(casterCell).advancedOrientationTo(MapPoint.fromCellId(spellImpactCell))
        )
        outputPortalCell = MapTools.INVALID_CELL_ID
        if portalCell != MapTools.INVALID_CELL_ID:
            oppositeDirection = int(MapDirection.getOppositeDirection(direction))
            distance = MapTools.getDistance(portalCell, casterCell)
            outputPortalCell = spellImpactCell
            while distance > 0:
                outputPortalCell = MapTools.getNextCellByDirection(outputPortalCell, oppositeDirection)
                distance -= 1
        if isPreview and spell["defaultPreviewZone"] is not None:
            finalZone = self.getZone(
                spell["effectZone"].activationZoneShape,
                spell["effectZone"].activationZoneSize,
                spell["effectZone"].activationZoneMinSize,
                isWholeMapShapeIgnored,
                spell["effectZone"].activationZoneStopAtTarget,
                not isinstance(spell, SpellWrapper),
                casterId,
                outputPortalCell,
            )
        else:
            finalZone = self.getPreferredPreviewZone(
                spell, isWholeMapShapeIgnored, isInfiniteSizeIgnored, False, outputPortalCell
            )
        if finalZone is None:
            finalZone = self.getZone(
                SpellShapeEnum.X,
                0,
                0,
                isWholeMapShapeIgnored,
                0,
                not isinstance(spell, SpellWrapper),
                casterId,
                outputPortalCell,
            )
        finalZone.direction = direction
        if isPreview and spell.previewZones is not None and len(spell.previewZones) > 0:
            entitiesFrame = Kernel().fightEntitiesFrame
            if entitiesFrame is None:
                return finalZone
            entitiesIds = entitiesFrame.getEntitiesIdsList()
            zonesCells = finalZone.getCells(spellImpactCell)
            additionalZoneCells = []
            isDefaultZoneDisplayed = True
            for effectZone in spell.previewZones:
                if effectZone.isDisplayZone:
                    relatedEffect = EffectInstance()
                    relatedEffect.targetMask = effectZone.activationMask
                    relatedEffect.zoneShape = effectZone.activationZoneShape
                    relatedEffect.zoneSize = effectZone.activationZoneSize
                    relatedEffect.zoneMinSize = effectZone.activationZoneMinSize
                    relatedEffect.zoneStopAtTarget = effectZone.activationZoneStopAtTarget
                    if effectZone.casterMask:
                        casterEffect = relatedEffect.clone()
                        casterEffect.targetMask = effectZone.casterMask
                        casterPos = Kernel().fightEntitiesFrame.getLastKnownEntityPosition(casterId)
                        if not DamageUtil.verifySpellEffectMask(casterId, casterId, casterEffect, casterPos):
                            continue
                    displayedZone = self.getZone(
                        effectZone.displayZoneShape,
                        effectZone.displayZoneSize,
                        effectZone.displayZoneMinSize,
                        isWholeMapShapeIgnored,
                        effectZone.displayZoneStopAtTarget,
                        False,
                        casterId,
                        outputPortalCell if outputPortalCell != MapTools.INVALID_CELL_ID else casterCell,
                    )
                    displayedZone.direction = direction
                    isActivationMaskEmpty = not relatedEffect.targetMask
                    if isActivationMaskEmpty:
                        additionalZoneCells.extend(displayedZone.getCells(spellImpactCell))
                        if isDefaultZoneDisplayed and effectZone.isDefaultPreviewZoneHidden:
                            isDefaultZoneDisplayed = False
                    activationZone = self.getZone(
                        effectZone.activationZoneShape,
                        effectZone.activationZoneSize,
                        effectZone.activationZoneMinSize,
                        isWholeMapShapeIgnored,
                        effectZone.activationZoneStopAtTarget,
                    )
                    activationZone.direction = direction
                    for entityId in entitiesIds:
                        entityInfo = entitiesFrame.getEntityInfos(entityId)
                        if (
                            entityInfo.spawnInfo.alive
                            and self.checkZone(
                                entityInfo, relatedEffect.zoneShape, activationZone.getCells(spellImpactCell)
                            )
                            and (
                                isActivationMaskEmpty
                                or DamageUtil.verifySpellEffectMask(casterId, entityId, relatedEffect, spellImpactCell)
                            )
                        ):
                            additionalZoneCells.extend(displayedZone.getCells(entityInfo.disposition.cellId))
                            if isDefaultZoneDisplayed and effectZone.isDefaultPreviewZoneHidden:
                                isDefaultZoneDisplayed = False
            finalZoneCells = zonesCells if isDefaultZoneDisplayed else []
            if additionalZoneCells:
                finalZoneCells.extend(additionalZoneCells)
            return Custom(finalZoneCells)
        return finalZone

    def getZone(
        self,
        shape: int,
        size: int,
        alternativeSize: int,
        isWholeMapShapeIgnored: bool = False,
        isZoneStopAtTarget: int = 0,
        isWeapon: bool = False,
        entityId: float = float("nan"),
        entityCellId: int = -1,
    ) -> DisplayZone:
        casterId = float("nan")
        casterInfoCellId = 0
        if shape == SpellShapeEnum.X:
            return Cross(
                shape,
                alternativeSize,
                size if isWeapon or size else (alternativeSize if alternativeSize else size),
                DataMapProvider(),
            )
        elif shape == SpellShapeEnum.L:
            return Line(shape, 0, size, DataMapProvider())
        elif shape == SpellShapeEnum.l:
            casterId = entityId if not math.isnan(entityId) else CurrentPlayedFighterManager().currentFighterId
            if PlayedCharacterApi().isInFight():
                casterInfoCellId = Kernel().fightEntitiesFrame.getEntityInfos(casterId).disposition.cellId
            return Line(
                shape,
                alternativeSize,
                size,
                DataMapProvider(),
                True,
                isZoneStopAtTarget == 1,
                entityCellId if entityCellId != -1 else casterInfoCellId,
            )
        elif shape == SpellShapeEnum.T:
            return Cross(shape, 0, size, DataMapProvider())
        elif shape == SpellShapeEnum.D:
            return Cross(shape, 0, size, DataMapProvider())
        elif shape == SpellShapeEnum.C:
            return Lozenge(shape, alternativeSize, size, DataMapProvider())
        elif shape == SpellShapeEnum.O:
            return Lozenge(shape, size, size, DataMapProvider())
        elif shape == SpellShapeEnum.Q:
            return Cross(shape, alternativeSize if alternativeSize else 1, size if size else 1, DataMapProvider())
        elif shape == SpellShapeEnum.V:
            return Cone(0, size, DataMapProvider())
        elif shape == SpellShapeEnum.W:
            return Square(0, size, True, DataMapProvider())
        elif shape == SpellShapeEnum.plus:
            return Cross(shape, 0, size if size else 1, DataMapProvider(), True)
        elif shape == SpellShapeEnum.sharp:
            return Cross(shape, alternativeSize, size, DataMapProvider(), True)
        elif shape == SpellShapeEnum.slash:
            return Line(shape, 0, size, DataMapProvider())
        elif shape == SpellShapeEnum.star:
            return Cross(shape, 0, size, DataMapProvider(), False, True)
        elif shape == SpellShapeEnum.minus:
            return Cross(shape, 0, size, DataMapProvider(), True)
        elif shape == SpellShapeEnum.G:
            return Square(0, size, False, DataMapProvider())
        elif shape == SpellShapeEnum.I:
            return Lozenge(shape, size, 63, DataMapProvider())
        elif shape == SpellShapeEnum.U:
            return HalfLozenge(0, size, DataMapProvider())
        elif shape in (SpellShapeEnum.A, SpellShapeEnum.a):
            if not isWholeMapShapeIgnored:
                return Lozenge(shape, 0, 63, DataMapProvider())
            return Cross(shape, 0, 0, DataMapProvider())
        elif shape == SpellShapeEnum.R:
            return Rectangle(alternativeSize, size, DataMapProvider())
        elif shape == SpellShapeEnum.F:
            return Fork(size, DataMapProvider())
        elif shape == SpellShapeEnum.P:
            return Cross(shape, 0, 0, DataMapProvider())
        else:
            raise Exception("Unknown shape %s", shape)

    def checkZone(self, pEntityInfos: GameFightFighterInformations, pShape: int, pCells: List[int]) -> bool:
        if pShape == SpellShapeEnum.a:
            return pEntityInfos.spawnInfo.alive
        elif pShape == SpellShapeEnum.A:
            return True
        else:
            return pEntityInfos.disposition.cellId in pCells

    def getEffectZone(self, rawZone:str) -> EffectZone:
        effectZone = EffectZone()
        effectZone.rawActivationZone = rawZone
        return effectZone

    def parseZone(self, rawZone: str, casterId: float, targetedCellId: int, isWeapon: bool) -> DisplayZone:
        effectZone = self.getEffectZone(rawZone)
        return self.getZone(
            effectZone.activationZoneShape,
            effectZone.activationZoneSize,
            effectZone.activationZoneMinSize,
            False,
            effectZone.activationZoneStopAtTarget,
            isWeapon,
            casterId,
            targetedCellId,
        )
