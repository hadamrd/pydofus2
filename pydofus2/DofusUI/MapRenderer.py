import io
import os
import threading

from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtGui import QColor, QImage, QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import QGraphicsPixmapItem

from pydofus2.com.ankamagames.atouin.Atouin import Atouin
from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.AnimatedGraphicalElementData import (
    AnimatedGraphicalElementData,
)
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.BoundingBoxGraphicalElementData import (
    BoundingBoxGraphicalElementData,
)
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.EntityGraphicalElementData import (
    EntityGraphicalElementData,
)
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import (
    NormalGraphicalElementData,
)
from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.data.map.elements.GraphicalElement import GraphicalElement
from pydofus2.com.ankamagames.atouin.data.map.Fixture import Fixture
from pydofus2.com.ankamagames.atouin.data.map.Layer import Layer, LayerCell
from pydofus2.com.ankamagames.atouin.enums.ElementTypesEnum import ElementTypesEnum
from pydofus2.com.ankamagames.atouin.FrustumManager import FrustumManager
from pydofus2.com.ankamagames.atouin.managers.InteractiveCellManager import InteractiveCellManager
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.types.BitmapCellContainer import BitmapCellContainer
from pydofus2.com.ankamagames.atouin.types.CellContainer import CellContainer
from pydofus2.com.ankamagames.atouin.types.DataMapContainer import DataMapContainer
from pydofus2.com.ankamagames.atouin.types.InteractiveCell import InteractiveCell
from pydofus2.com.ankamagames.atouin.types.SimpleGraphicsContainer import SimpleGraphicsContainer
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.com.ankamagames.tiphon.types.look.TiphonEntityLook import TiphonEntityLook
from pydofus2.DofusUI.AnimatedGifItem import AnimatedGifItem
from pydofus2.DofusUI.GfxParallelLoader import GfxParallelLoader
from pydofus2.DofusUI.OptionManager import OptionManager
from pydofus2.DofusUI.StageShareManager import StageShareManager
from pydofus2.DofusUI.SwfToGifConverter import SwfConverter
from pydofus2.flash.geom.ColorTransform import ColorTransform

os.environ["QT_API"] = "pyqt5"


class MapRenderer:
    _groundGlobalScaleRatio = None
    _renderScale = 1
    _hideForeground = True
    _renderBackgroundColor = True
    _hasGroundJPG = False
    _renderFixture = True
    _tacticModeActivated = False
    _foregroundBitmap = None

    def __init__(self, container: SimpleGraphicsContainer, elements: Elements) -> None:
        self._bitmapsGfx = dict[str, QImage]()
        self._swfGfx = dict[str, AnimatedGifItem]()
        self._hideForeground = Atouin().options.getOption("hideForeground")
        self._container = container
        if self._groundGlobalScaleRatio is None:
            val = XmlConfig().getEntry("config.gfx.world.scaleRatio")
            self._groundGlobalScaleRatio = 1 if val is None else float(val)
        self.bitmapSize = QSize(AtouinConstants.WIDESCREEN_BITMAP_WIDTH, StageShareManager().startHeight)
        self._gfxLoader = None
        self.swfTopGif = SwfConverter(self.onAllGfxLoaded)
        self._gfxPath = Atouin().options.getOption("elementsPath")
        self._gfxPathSwf = Atouin().options.getOption("swfPath")
        self._map = MapDisplayManager().dataMap
        self._elements = elements
        self.elemCount = 0
        self._cancelRender = False
        self._loadedGfxListCount = 0
        self._extension = Atouin.DEFAULT_MAP_EXTENSION
        self._groundBitmap: QPixmap = None
        self._mapLoaded = False
        self._mapIsReady = False
        self._groundIsLoaded = False
        self._icm = InteractiveCellManager()
        self.initGfxLoader()

    @property
    def renderScale(self):
        return self._renderScale

    @property
    def hasToRenderForegroundFixtures(self) -> bool:
        return self._renderFixture and self._map.foregroundFixtures

    def getGfxUri(self, gfxId) -> Uri:
        isJpg = Elements().isJpg(gfxId)
        path_str = (
            self._gfxPath
            + "/"
            + ("jpg" if isJpg else "png")
            + "/"
            + str(gfxId)
            + "."
            + ("jpg" if isJpg else self._extension)
        )
        return Uri(path_str, gfxId)

    def getSwfUri(self, gfxId):
        return Uri(f"{self._gfxPath}/swf/{gfxId}.swf", gfxId)

    def render(
        self,
        dataContainer: DataMapContainer,
        forceReloadWithoutCache=False,
        renderId=0,
        renderFixture=True,
        displayWorld=True,
    ):
        self._thread_name = threading.current_thread().name
        self._renderFixture = renderFixture
        self._renderBackgroundColor = renderFixture
        self._frustumX = FrustumManager().frustum.x
        self._renderId = renderId
        self._displayWorld = displayWorld
        Atouin().cancelZoom()
        self._allowAnimatedGfx = Atouin().options.getOption("allowAnimatedGfx")
        self._allowParticlesFx = Atouin().options.getOption("allowParticlesFx")
        newLoader = not self._mapLoaded
        self._mapLoaded = False
        self._groundIdLoaded = False
        self._maIsReady = False
        self._map = dataContainer.dataMap
        self._forceReloadWithoutCache = forceReloadWithoutCache
        self.handleGroundCaching()
        bitmapsGfx = dict[int, QImage]()
        self._useSmooth = Atouin().options.getOption("useSmooth")
        self._dataMapContainer = dataContainer
        self._identifiedElements = dict()
        self._loadedGfxListCount = 0
        self._hasSwfGfx = False
        gfxUri = []
        swfUri = []
        gfxList = self._map.getGfxList(self._hasGroundJPG)
        for nged in gfxList:
            if isinstance(nged, AnimatedGraphicalElementData):
                uri = self.getSwfUri(nged)
                swfUri.append(uri)
                self._hasSwfGfx = True
            elif nged.gfxId in self._bitmapsGfx:
                bitmapsGfx[nged.gfxId] = self._bitmapsGfx[nged.gfxId]
            else:
                uri = self.getGfxUri(nged.gfxId)
                gfxUri.append(uri)
                self._hasBitmapGfx = True
        if renderFixture:
            if not self._hasGroundJPG:
                self.preprocessFixtureLayer(self._map.backgroundFixtures, gfxUri, bitmapsGfx)
            self.preprocessFixtureLayer(self._map.foregroundFixtures, gfxUri, bitmapsGfx)
        self._bitmapsGfx = bitmapsGfx
        self._swfGfx = []
        if newLoader:
            self.initGfxLoader()
        self._filesToLoad = len(gfxUri) + len(swfUri)
        if self._renderScale == 1:
            Logger().debug("Starting to load gfx elements")
            self._gfxLoader.loadItems(gfxUri)
        if swfUri:
            self.swfTopGif.loadSwfList(swfUri)
        if not gfxUri and not swfUri:
            self.onAllGfxLoaded()

    def preprocessFixtureLayer(self, layer: list[Fixture], gfxUri: list, bitmapsGfx: dict):
        for fixture in layer:
            if fixture.fixtureId in self._bitmapsGfx:
                bitmapsGfx[fixture.fixtureId] = self._bitmapsGfx[fixture.fixtureId]
            else:
                uri = self.getGfxUri(fixture.fixtureId)
            gfxUri.append(uri)
            self._hasBitmapGfx = True

    def handleGroundCaching(self):
        Atouin().options.getOption("groundCacheMode")
        Logger().warning("Ground caching is not yet implemented")

    def makeMap(self):
        layerId = 0
        cellDisabled = False
        hideFg = False
        groundOnly = False
        aInteractiveCell = {}
        finalGroundBitmap = None
        self._screenResolutionOffset = QPoint()
        self._screenResolutionOffset.setX((self.bitmapSize.width() - StageShareManager().startWidth) / 2)
        self._screenResolutionOffset.setY((self.bitmapSize.height() - StageShareManager().startHeight) / 2)
        if not self._hasGroundJPG:
            self.createGroundBitmap()
        if self._renderBackgroundColor:
            self._container.opaqueBackground = self._map.backgroundColor
        lastCellId = 0
        currentCellId = 0
        for layer in self._map.layers:
            if layer.cellsCount != 0:
                layerId = layer.layerId
                currentLayerIsGround = layerId == Layer.LAYER_GROUND
                if not currentLayerIsGround:
                    layerCtr = self._dataMapContainer.getLayer(layerId)
                hideFg = layerId and self._hideForeground
                skipLayer = groundOnly
                i = 0
                nbCell = len(layer.cells)
                while i < nbCell:
                    cell = layer.cells[i]
                    currentCellId = int(cell.cellId)
                    if layerId == Layer.LAYER_GROUND:
                        if currentCellId - lastCellId > 1:
                            currentCellId = int(lastCellId + 1)
                            cell = None
                        else:
                            i += 1
                    else:
                        i += 1
                    if currentLayerIsGround:
                        cellCtr = BitmapCellContainer(currentCellId)
                    else:
                        cellCtr = CellContainer(currentCellId)
                    cellCtr.layerId = layerId
                    if cell:
                        cellPnt = cell.pixelCoords
                        scaleRatio = self._groundGlobalScaleRatio if isinstance(cellCtr, CellContainer) else 1
                        cellCtr.startX = int(round(cellPnt.x)) * scaleRatio
                        cellCtr.startY = int(round(cellPnt.y)) * scaleRatio
                        cellCtr.setPos(cellCtr.startX, cellCtr.startY)
                        if not skipLayer:
                            if not self._hasGroundJPG or not currentLayerIsGround:
                                cellDisabled = self.addCellBitmapsElements(cell, cellCtr, hideFg, currentLayerIsGround)
                    else:
                        cellDisabled = False
                        cellPnt = Cell.cellPixelCoords(currentCellId)
                        cellCtr.startX = cellPnt.x
                        cellCtr.startY = cellPnt.y
                        cellCtr.setPos(cellCtr.startX, cellCtr.startY)
                    if not currentLayerIsGround:
                        layerCtr.addCell(cellCtr)
                    elif not self._hasGroundJPG:
                        self.drawCellOnGroundBitmap(self._groundBitmap, cellCtr)
                    cellRef = self._dataMapContainer.getCellReference(currentCellId)
                    cellRef.addSprite(cellCtr)
                    cellRef.x = cellCtr.x()
                    cellRef.y = cellCtr.y()
                    cellRef.isDisabled = cellDisabled
                    if layerId != Layer.LAYER_ADDITIONAL_DECOR and currentCellId not in aInteractiveCell:
                        aInteractiveCell[currentCellId] = True
                        cellInteractionCtr = self._icm.getCell(currentCellId)
                        cellData = self._map.cells[currentCellId]
                        cellElevation = 0 if self._tacticModeActivated else cellData.floor
                        cellInteractionCtr.setPos(cellCtr.x(), cellCtr.y() - cellElevation)
                        if not self._dataMapContainer.getChildByName(str(currentCellId)):
                            DataMapContainer.interactiveCell[currentCellId] = InteractiveCell(
                                currentCellId, cellInteractionCtr, cellInteractionCtr.x(), cellInteractionCtr.y()
                            )
                        cellRef.elevation = cellInteractionCtr.y()
                        cellRef.mov = cellData.mov
                    lastCellId = int(currentCellId)
                if not currentLayerIsGround:
                    layerCtr.setScale(1 / self._groundGlobalScaleRatio)
                    layerCtr.setParentItem(self._container)
                    self._container.addChild(layerCtr)
                elif not self._hasGroundJPG:
                    finalGroundBitmap = self.createFinalGroundPixmap()
        if self.hasToRenderForegroundFixtures:
            self.createForegroundBitmap()
            # self._foregroundBitmap.setVisible(not self._tacticModeActivated)
            # self._container.addChild(self._foregroundBitmap) FIXME
        if finalGroundBitmap:
            if self._groundBitmap:
                self._groundBitmap = None
            self._groundBitmap = finalGroundBitmap
        if self._groundBitmap:
            self._groundBitmap.setX(-self._frustumX - self._screenResolutionOffset.x())
            self._groundBitmap.setY(-self._screenResolutionOffset.y())
            self._groundBitmap.setScale(1 / self._renderScale)

        selectionContainer = SimpleGraphicsContainer()
        selectionContainer.name = "selectionCtr"
        self._container.addChild(selectionContainer)
        if not self._hasGroundJPG or self._groundIsLoaded:
            if self._displayWorld:
                Atouin().worldContainer.setVisible(True)
        Atouin().applyMapZoomScale(self._map)
        self._mapIsReady = True

    def createFinalGroundPixmap(self):
        width = int(AtouinConstants.RESOLUTION_HIGH_QUALITY[0] * self._renderScale)
        height = int(AtouinConstants.RESOLUTION_HIGH_QUALITY[1] * self._renderScale)
        pixmap = QPixmap(width, height)
        if self._renderBackgroundColor:
            pixmap.fill(QColor(self._map.backgroundColor))
        else:
            pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        transform = QTransform()
        transform.scale(1 / self._groundGlobalScaleRatio, 1 / self._groundGlobalScaleRatio)
        painter.setTransform(transform)
        if isinstance(self._groundBitmap, QGraphicsPixmapItem):
            groundBitMap = self._groundBitmap.pixmap()
        elif isinstance(self._groundBitmap, QPixmap):
            groundBitMap = self._groundBitmap
        else:
            raise ValueError(f"self._groundBitmap has unexpected type {type(self._groundBitmap)}")
        painter.drawPixmap(int(-self._frustumX * self._renderScale), 0, groundBitMap)  # Draw the prepared pixmap
        painter.end()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        pixmap_item.setTransformationMode(Qt.SmoothTransformation)
        self._container.addChild(pixmap_item)
        return pixmap_item

    def createForegroundBitmap(self):
        Logger().warning("MapRenderer createForegroundBitmap not implemented yet")
        self._foregroundBitmap = None

    def createGroundBitmap(self):
        finalScale = self._groundGlobalScaleRatio * self._renderScale
        bitmapFinalWidth = int(self.bitmapSize.width() * finalScale)
        bitmapFinalHeight = int(self.bitmapSize.height() * finalScale)
        self._groundBitmap = QPixmap(bitmapFinalWidth, bitmapFinalHeight)  # Keep as QPixmap
        self._groundBitmap.fill(Qt.transparent)
        painter = QPainter(self._groundBitmap)
        if self._renderBackgroundColor:
            rgb_color = QColor(self._map.backgroundColor)
            painter.fillRect(0, 0, bitmapFinalWidth, bitmapFinalHeight, rgb_color)
        painter.end()
        self.renderFixture(self._map.backgroundFixtures, self._groundBitmap)

    def renderFixture(self, fixtures: list[Fixture], groundPixmap: QPixmap):
        if not fixtures or not self._renderFixture:
            return
        smoothing = OptionManager.getOptionManager("atouin").getOption("useSmooth")
        painter = QPainter(groundPixmap)
        for fixture in fixtures:
            fixtureQImage = self._bitmapsGfx.get(fixture.fixtureId)
            if fixtureQImage is None:
                print(f"Fixture {fixture.fixtureId} file is missing")
                continue
            if fixture.redMultiplier or fixture.greenMultiplier or fixture.blueMultiplier or fixture.alpha != 1:
                cltfm = ColorTransform(
                    fixture.redMultiplier, fixture.greenMultiplier, fixture.blueMultiplier, fixture.alpha
                )
                fixtureQImage = cltfm.apply(fixtureQImage)
            m = QTransform()
            halfWidth = fixtureQImage.width() * 0.5
            halfHeight = fixtureQImage.height() * 0.5
            m.translate(-halfWidth, -halfHeight)
            m.scale(fixture.xScale / 1000, fixture.yScale / 1000)
            m.rotate(fixture.rotation / 100)
            m.translate(
                (fixture.offsetX + AtouinConstants.CELL_HALF_WIDTH + self._frustumX) * self.renderScale + halfWidth,
                (fixture.offsetY + AtouinConstants.CELL_HEIGHT) * self.renderScale + halfHeight,
            )
            m.translate(self._screenResolutionOffset.x(), self._screenResolutionOffset.y())
            painter.setTransform(m, combine=False)
            if smoothing:
                painter.setRenderHint(QPainter.Antialiasing, True)
            fixtureQPixmap = QPixmap.fromImage(fixtureQImage)
            painter.drawPixmap(0, 0, fixtureQPixmap)
        painter.end()

    def addCellBitmapsElements(self, cell: LayerCell, cellCtr: CellContainer, transparent=False, ground=False):
        colors = None
        Atouin().options.getOption("useWorldEntityPool")
        lsElements = cell.elements
        boundingBoxElements = set()
        elementDo = None
        disabled = False
        for element in lsElements:
            if element.elementType == ElementTypesEnum.GRAPHICAL:
                ge: GraphicalElement = element
                ed = self._elements.getElementData(ge.elementId)
                if ed:
                    if isinstance(ed, NormalGraphicalElementData):
                        if isinstance(ed, AnimatedGraphicalElementData):
                            elementDo = self._swfGfx.get(ed.gfxId)
                            if not elementDo:
                                Logger().error(f"Unable to find swf of the element {ed.gfxId}")
                                continue
                        else:
                            elementPixmap = QPixmap.fromImage(self._bitmapsGfx[ed.gfxId])
                            elementDo = QGraphicsPixmapItem(elementPixmap)
                            elementDo.name = f"mapGfx::{ge.elementId}::{ed.gfxId}"
                        if self._renderScale != 1:
                            elementDo.setScale(self._renderScale)
                        elementDo.setPos(elementDo.pos().x() - ed.origin.x, elementDo.pos().y() - ed.origin.y)
                        if ed.horizontalSymmetry:
                            self.applyHorizontalSymmetry(elementDo)
                        if self._renderScale != 1:
                            if not (
                                isinstance(ed, AnimatedGraphicalElementData) and self._map.getGfxCount(ed.gfxId) == 1
                            ):
                                elementDo.setScale(1 / self._renderScale)
                        if isinstance(ed, BoundingBoxGraphicalElementData):
                            elementDo.setVisible(False)
                            boundingBoxElements.add(ge.identifier)
                        elementDo.setAcceptHoverEvents(False)
                        elementDo.setAcceptedMouseButtons(Qt.NoButton)
                        # if isinstance(ed, BlendedGraphicalElementData) and hasattr(elementDo, "blendMode"):
                        #     elementDo.blendMode = ed.blendMode FIXME there is no blending in pyqt5
                    elif isinstance(ed, EntityGraphicalElementData):
                        TiphonEntityLook.fromString(ed.entityLook)
                        # TODO: complete handling of EntityGraphicalElementData here
                    if not elementDo:
                        Logger().warn(
                            "A graphical element was missed (Element ID "
                            + str(ge.elementId)
                            + "; Cell "
                            + str(ge.cell.cellId)
                            + ")."
                        )
                        continue
                    if not ge.colorMultiplicator.isOne():
                        colors = {
                            "red": ge.colorMultiplicator.red / 255,
                            "green": ge.colorMultiplicator.green / 255,
                            "blue": ge.colorMultiplicator.blue / 255,
                            "alpha": 1,
                        }
                    0.5 if transparent else 1
                    if ge.identifier > 0:
                        if ground:
                            Logger().warning(
                                f"Will not render elementId {ed.id} since it's an interactive one (identifier: {ge.identifier}), on the ground layer!"
                            )
                            continue
                        ie = {"sprite": elementDo, "position": MapPoint.fromCellId(cell.cellId)}
                        self._identifiedElements[ge.identifier] = ie
                    elementDo.setPos(
                        elementDo.pos().x() + round(AtouinConstants.CELL_HALF_WIDTH + ge.pixelOffset.x),
                        elementDo.pos().y()
                        + round(AtouinConstants.CELL_HALF_WIDTH - ge.altitude * 10 + ge.pixelOffset.y),
                    )
            if elementDo:
                cellCtr.addFakeChild(elementDo, colors=colors)
            elif element.elementType != ElementTypesEnum.SOUND:
                if not self._cellBitmapData:
                    cell_width = AtouinConstants.CELL_WIDTH
                    cell_height = AtouinConstants.CELL_HEIGHT
                    color = QColor(13369548)
                    self._cellBitmapData = QPixmap(cell_width, cell_height)
                    self._cellBitmapData.fill(color)
                elementDo = QGraphicsPixmapItem(self._cellBitmapData)
                cellCtr.addFakeChild(elementDo)
            else:
                print("not rendering this shit : ", ed.gfxId)
        return disabled

    def applyHorizontalSymmetry(self, item: QGraphicsPixmapItem):
        current_transform = item.transform()
        flipped_transform = current_transform.scale(-1, 1)
        item.setTransform(flipped_transform)
        item.setPos(item.pos().x() + item.boundingRect().width(), item.pos().y())

    def onBitmapGfxLoaded(self, gfxId, image_bytes: io.BytesIO):
        if self._cancelRender:
            return
        self._bitmapsGfx[gfxId] = QImage.fromData(image_bytes)

    def onAllGfxLoaded(self):
        Logger().debug("All gfx elements loaded")
        if self._cancelRender or self._mapIsReady:
            return
        self._loadedGfxListCount += 1
        if self._hasBitmapGfx and self.hasSwfGfx and self._loadedGfxListCount != 2:
            return
        self._mapLoaded = True
        self.makeMap()

    def onloadError(self, gfxId, exc: Exception):
        Logger().error(f"Load of gfx {gfxId} failed with err {exc}")

    def initGfxLoader(self):
        self._gfxLoader = GfxParallelLoader(maxThreads=6)
        self._gfxLoader.progress.connect(self.onBitmapGfxLoaded)
        self._gfxLoader.error.connect(self.onloadError)
        self._gfxLoader.finished.connect(self.onAllGfxLoaded)

    def onMapLoadingProgress(self, event, uri, total, loadedCount):
        pass

    def drawCellOnGroundBitmap(self, groundBitmap, cellCtr):
        # Logger().warning("MapRendered method drawCellOnGroundBitmap not implemented yet")FIXME
        pass

    @property
    def hasSwfGfx(self):
        return self._hasSwfGfx
