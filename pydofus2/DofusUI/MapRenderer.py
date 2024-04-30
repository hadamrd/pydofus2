import io

from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtGui import QColor, QImage, QMovie, QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QGraphicsItemGroup, QGraphicsPixmapItem

from pydofus2.com.ankamagames.atouin.Atouin import Atouin
from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.AnimatedGraphicalElementData import (
    AnimatedGraphicalElementData,
)
from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.data.map.Fixture import Fixture
from pydofus2.com.ankamagames.atouin.data.map.Layer import Layer
from pydofus2.com.ankamagames.atouin.FrustumManager import FrustumManager
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.types.BitmapCellContainer import BitmapCellContainer
from pydofus2.com.ankamagames.atouin.types.CellContainer import CellContainer
from pydofus2.com.ankamagames.atouin.types.DataMapContainer import DataMapContainer
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderFactory import ResourceLoaderFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import ResourceLoaderType
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.DofusUI.OptionManager import OptionManager
from pydofus2.DofusUI.StageShareManager import StageShareManager
from pydofus2.DofusUI.SwfToGifConverter import SwfConverter


class MapRenderer:
    _groundGlobalScaleRatio = None
    _renderScale = 1
    _hideForeground = True
    _renderBackgroundColor = True
    _hasGroundJPG = False
    _renderFixture = True

    def __init__(self, container: QGraphicsItemGroup, elements: Elements) -> None:
        self._bitmapsGfx = dict[str, QPixmap]()
        self._swfGfx = dict[str, QMovie]()
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
        self.mousePressEvent = self.onSceneMousePress
        self._map = MapDisplayManager().dataMap
        self._elements = elements
        self.elemCount = 0
        self._cancelRender = False
        self._loadedGfxListCount = 0
        self._extension = Atouin.DEFAULT_MAP_EXTENSION

    def initGfxLoader(self):
        if self._gfxLoader:
            self._gfxLoader.reset()
            self._gfxLoader.cancel()
        self._gfxLoader = ResourceLoaderFactory.getLoader(ResourceLoaderType.PARALLEL_LOADER)
        self.addGfxLoaderListeners()

    def addGfxLoaderListeners(self):
        self._gfxLoader.on(ResourceEvent.ERROR, self.onloadError)
        self._gfxLoader.on(ResourceEvent.LOADED, self.onBitmapGfxLoaded)
        self._gfxLoader.on(ResourceEvent.LOADER_COMPLETE, self.onAllGfxLoaded)
        self._gfxLoader.on(ResourceEvent.LOADER_PROGRESS, self.onMapLoadingProgress)

    def initSwfLoader(self):
        pass

    def onSceneMousePress(self, event):
        item = self.itemAt(event.scenePos(), self.parent().stage.transform())
        if isinstance(item, QGraphicsPixmapItem):
            if event.button() == Qt.LeftButton:
                gfxId = item.toolTip()
                clipboard = QApplication.clipboard()
                clipboard.setText(gfxId)
            elif event.button() == Qt.RightButton:
                item.setVisible(False)

    def onMapLoadingProgress(self, event, uri, total, loadedCount):
        pass

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

    def onBitmapGfxLoaded(self, event, uri: Uri, resourceType, image_bytes: io.BytesIO):
        if self._cancelRender:
            return
        QImage.fromData(image_bytes)
        self._bitmapsGfx[uri.tag.gfxId] = pixmap

    def onAllGfxLoaded(self, event, total, completed):
        if self._cancelRender or self._mapIsReady:
            return
        self._loadedGfxListCount += 1
        if self._hasBitmapGfx and self.hasSwfGfx and self._loadedGfxListCount != 2:
            return
        self._mapLoaded = True
        self.makeMap()

    def onloadError(self, event, uri, errorMsg, errorCode):
        Logger().error(f"Load of resource at uri: {uri} failed with err[{errorCode}] {errorMsg}")

    def render(
        self,
        dataContainer: DataMapContainer,
        forceReloadWithoutCache=False,
        renderId=0,
        renderFixture=True,
        displayWorld=True,
    ):
        self._renderFixture = renderFixture
        self._renderBackgroundColor = renderFixture
        self._frustumX = FrustumManager().frustum.x
        self._renderId = renderId
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
        bitmapsGfx = []
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
                uri = Uri(self._gfxPath + "/swf/" + nged.gfxId + ".swf")
                uri.tag = nged.gfxId
                swfUri.append(uri)
                self._hasSwfGfx = True
            elif nged.gfxId in self._bitmapsGfx:
                bitmapsGfx[nged.gfxId] = self._bitmapsGfx[nged.gfxId]
            else:
                uri = self.getGfxUri(nged.gfxId)
                self._hasBitmapGfx = True
        if renderFixture:
            if not self._hasGroundJPG:
                self.preprocessFixtureLayer(self._map.backgroundFixtures)
            self.preprocessFixtureLayer(self._map.foregroundFixtures)
        self._bitmapsGfx = bitmapsGfx
        self._swfGfx = []
        if newLoader:
            self.initGfxLoader()
            self.initSwfLoader()
        self._filesToLoad = len(gfxUri) + len(swfUri)
        if self._renderScale == 1:
            self._gfxLoader.load(gfxUri)
        self.swfTopGif.loadSwfList(swfUri)
        if len(gfxUri) == 0 or len(swfUri) == 0:
            self.onAllGfxLoaded(None)

    def hasSwfLoaderListeners(self):
        pass

    def hasGfxLoaderListeners(self):
        pass

    def initSwfLoader(self):
        pass

    def preprocessFixtureLayer(self, layer: list[Fixture], gfxUri: list, bitmapsGfx: dict):
        for fixture in layer:
            if self._bitmapsGfx[fixture.fixtureId]:
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
        aInteractiveCell = []
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
                layerCtr = None
                currentLayerIsGround = layer.layerId == Layer.LAYER_GROUND
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
                    cellCtr.mouseEnabled = False
                    if cell:
                        cellPnt = cell.pixelCoords
                        scaleRatio = self._groundGlobalScaleRatio if isinstance(cellCtr, CellContainer) else 1
                        cellCtr.startX = int(round(cellPnt.x)) * scaleRatio
                        cellCtr.startY = int(round(cellPnt.y)) * scaleRatio
                        if not skipLayer:
                            if not self._hasGroundJPG or not currentLayerIsGround:
                                cellDisabled = self.addCellBitmapsElements(cell, cellCtr, hideFg, currentLayerIsGround)
                    else:
                        cellDisabled = False
                        cellPnt = Cell.cellPixelCoords(currentCellId)
                        cellCtr.x = cellCtr.startX = cellPnt.x
                        cellCtr.y = cellCtr.startY = cellPnt.y
                    if not currentLayerIsGround:
                        layerCtr.addChild(cellCtr)
                    elif not self._hasGroundJPG:
                        self.drawCellOnGroundBitmap(self._groundBitmap, cellCtr)
                    cellRef = self._dataMapContainer.getCellReference(currentCellId)
                    cellRef.addSprite(cellCtr)
                    cellRef.x = cellCtr.x
                    cellRef.y = cellCtr.y
                    cellRef.isDisabled = cellDisabled
                    if layerId != Layer.LAYER_ADDITIONAL_DECOR and not aInteractiveCell[currentCellId]:
                        aInteractiveCell[currentCellId] = True
                        cellInteractionCtr = self._icm.getCell(currentCellId)
                        cellData = self._map.cells[currentCellId]
                        cellElevation = 0 if self._tacticModeActivated else cellData.floor
                        cellInteractionCtr.x = cellCtr.x
                        cellInteractionCtr.y = cellCtr.y - cellElevation
                        if not self._dataMapContainer.getChildByName(str(currentCellId)):
                            DataMapContainer.interactiveCell[currentCellId] = InteractiveCell(
                                currentCellId, cellInteractionCtr, cellInteractionCtr.x, cellInteractionCtr.y
                            )
                        cellRef.elevation = cellInteractionCtr.y
                        cellRef.mov = cellData.mov
                    lastCellId = int(currentCellId)
                if not currentLayerIsGround:
                    layerCtr.mouseEnabled = False
                    layerCtr.scaleX = layerCtr.scaleY = 1 / self._groundGlobalScaleRatio
                    self._container.addChild(layerCtr)
                elif not self._hasGroundJPG:
                    finalGroundBitmapData = BitmapData(
                        AtouinConstants.RESOLUTION_HIGH_QUALITY.x * self._renderScale,
                        AtouinConstants.RESOLUTION_HIGH_QUALITY.y * self._renderScale,
                        not self._renderBackgroundColor,
                        self._map.backgroundColor if self._renderBackgroundColor else 0,
                    )
                    self._m.identity()
                    self._m.scale(1 / self._groundGlobalScaleRatio, 1 / self._groundGlobalScaleRatio)
                    finalGroundBitmapData.lock()
                    finalGroundBitmapData.draw(self._groundBitmap.bitmapData, self._m, None, None, None, True)
                    finalGroundBitmapData.unlock()
                    finalGroundBitmap = Bitmap(finalGroundBitmapData, PixelSnapping.AUTO, True)
                    finalGroundBitmap.name = "finalGroundBitmap"
                    self._container.addChild(finalGroundBitmap)

        if self.hasToRenderForegroundFixtures:
            self.createForegroundBitmap()
            self._foregroundBitmap.visible = not self._tacticModeActivated
            self._container.addChild(self._foregroundBitmap)
        if finalGroundBitmap:
            if self._groundBitmap and self._groundBitmap.bitmapData:
                self._groundBitmap.bitmapData.dispose()
            self._groundBitmap = finalGroundBitmap
        if self._groundBitmap:
            self._groundBitmap.x = -self._frustumX - self._screenResolutionOffset.x
            self._groundBitmap.y = -self._screenResolutionOffset.y
            self._groundBitmap.scaleX = self._groundBitmap.scaleY = self._groundBitmap.scaleY / self._renderScale
        selectionContainer = Sprite()
        selectionContainer.name = "selectionCtr"
        self._container.addChild(selectionContainer)
        selectionContainer.mouseEnabled = False
        selectionContainer.mouseChildren = False
        if not self._hasGroundJPG or self._groundIsLoaded:
            if self._displayWorld:
                Atouin().worldContainer.visible = True
        Atouin().applyMapZoomScale(self._map)
        self._mapIsReady = True

    def createGroundBitmap(self):
        finalScale = self._groundGlobalScaleRatio * self._renderScale
        bitmapFinalWidth = int(self.bitmapSize.width() * finalScale)
        bitmapFinalHeight = int(self.bitmapSize.height() * finalScale)

        # Initialize the QPixmap
        groundPixmap = QPixmap(bitmapFinalWidth, bitmapFinalHeight)
        groundPixmap.fill(Qt.transparent)  # Set the initial fill to transparent

        # Start painting on QPixmap
        painter = QPainter(groundPixmap)

        if self._renderBackgroundColor:
            # Convert the integer RGB color to QColor. Assuming the color is stored as an RGB integer
            rgb_color = QColor(self._map.backgroundColor)
            painter.fillRect(0, 0, bitmapFinalWidth, bitmapFinalHeight, rgb_color)

        self._groundBitmap = QGraphicsPixmapItem(groundPixmap)
        self._groundBitmap.setData(0, "ground")  # Set a name equivalent in Qt
        self._groundBitmap.setPos(-self._frustumX * finalScale, 0)  # Setting x position
        self.renderFixture(self._map.backgroundFixtures, self._groundBitmap)
        painter.end()

    def renderFixture(self, fixtures: list[Fixture], container: QGraphicsPixmapItem):
        if not fixtures or not self._renderFixture:
            return
        smoothing = OptionManager.getOptionManager("atouin").getOption("useSmooth")
        for fixture in fixtures:
            bmpdt = self._bitmapsGfx.get(fixture.fixtureId)
            if bmpdt is None:
                print(f"Fixture {fixture.fixtureId} file is missing")
            else:
                painter = QPainter(container)
                m = QTransform()
                halfWidth = bmpdt.width() * 0.5
                halfHeight = bmpdt.height() * 0.5
                # Setup transformations
                m.translate(-halfWidth, -halfHeight)
                m.scale(fixture.xScale / 1000, fixture.yScale / 1000)
                m.rotate(fixture.rotation / 100)
                m.translate(
                    (fixture.offsetX + AtouinConstants.CELL_HALF_WIDTH + self._frustumX) * self.renderScale
                    + halfWidth,
                    (fixture.offsetY + AtouinConstants.CELL_HEIGHT) * self.renderScale + halfHeight,
                )
                m.translate(self._screenResolutionOffset.x(), self._screenResolutionOffset.y())
                if fixture.redMultiplier or fixture.greenMultiplier or fixture.blueMultiplier or fixture.alpha != 1:
                    self.multiply_fixture_colors(bmpdt, fixture)
                painter.setTransform(m, combine=False)
                if smoothing:
                    painter.setRenderHint(QPainter.Antialiasing, True)
                painter.drawPixmap(0, 0, bmpdt)
                painter.end()

    def multiply_fixture_colors(image: QImage, fixture: Fixture) -> QImage:
        """
        Applies RGB color multipliers to a QImage.

        Args:
            image: The QImage to be modified.
            multipliers: A QVector3D containing multipliers for each channel (R, G, B).

        Returns:
            A new QImage with the applied color multipliers.
        """

        if image.format() != QImage.Format_RGB888:
            raise ValueError("Unsupported image format. Only RGB888 is supported.")
        redm = fixture.redMultiplier / 127 + 1
        greenm = fixture.greenMultiplier / 127 + 1
        bluem = fixture.blueMultiplier / 127 + 1
        alpham = fixture.alpha / 255
        width, height = image.width(), image.height()

        # Efficient access to pixel data using scan lines
        for y in range(height):
            scan_line = image.scanLine(y)
            result_scan_line = image.scanLine(y)

            # Process pixels within the scan line efficiently
            for i in range(0, width * 4, 4):
                r, g, b, a = scan_line[i : i + 4]
                r = Qt.qMin(255, int(Qt.qRound(r * redm)))
                g = Qt.qMin(255, int(Qt.qRound(g * greenm)))
                b = Qt.qMin(255, int(Qt.qRound(b * bluem)))
                a = Qt.qMin(255, int(Qt.qRound(a * alpham)))
                result_scan_line[i : i + 4] = bytes([r, g, b, a])

        return image
