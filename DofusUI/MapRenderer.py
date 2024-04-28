import io

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QErrorMessage, QGraphicsPixmapItem, QGraphicsScene

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import (
    NormalGraphicalElementData,
)
from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.data.map.Fixture import Fixture
from pydofus2.com.ankamagames.atouin.data.map.Layer import Layer
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import ElementsAdapter
from pydofus2.com.ankamagames.atouin.types.BitmapCellContainer import BitmapCellContainer
from pydofus2.com.ankamagames.atouin.types.CellContainer import CellContainer
from pydofus2.com.ankamagames.atouin.types.DataMapContainer import DataMapContainer
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.managers.LangManager import LangManager
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import AdapterFactory
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderFactory import ResourceLoaderFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import ResourceLoaderType
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.flash.geom.Point import Point


class MapRenderer:
    _groundGlobalScaleRatio = None
    _renderScale = 1
    _hideForeground = True
    _renderBackgroundColor = True
    _hasGroundJPG = False
    _renderFixture = True

    def __init__(self, container: QGraphicsScene, elements: Elements) -> None:
        self._container = container
        self.error_dialog = QErrorMessage(parent)
        self.gfx_loader = ResourceLoaderFactory.getLoader(ResourceLoaderType.PARALLEL_LOADER)
        self.gfx_loader.on(ResourceEvent.ERROR, self.onloadError)
        self.gfx_loader.on(ResourceEvent.LOADED, self.onGfxLoaded)
        self.gfx_loader.on(ResourceEvent.LOADER_COMPLETE, self.onLoadComplete)
        self.gfx_loader.on(ResourceEvent.LOADER_PROGRESS, self.onMapLoadingProgress)
        self.mousePressEvent = self.onSceneMousePress
        self._map = MapDisplayManager().dataMap
        self.elemCount = 0
        if self._groundGlobalScaleRatio is None:
            val = XmlConfig().getEntry("config.gfx.world.scaleRatio")
            self._groundGlobalScaleRatio = 1 if val is None else float(val)
        self.bitmapSize = QSize(AtouinConstants.WIDESCREEN_BITMAP_WIDTH, MainWindow._startHeight)
        self._bitmapsGfx = {}

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
        path_str = GFX_PATH + "/" + ("jpg" if isJpg else "png") + "/" + str(gfxId) + "." + ("jpg" if isJpg else "png")
        return Uri(path_str, gfxId)

    def onGfxLoaded(self, event, uri: Uri, resourceType, image_bytes: io.BytesIO):
        pixmap = QPixmap()
        pixmap.loadFromData(image_bytes)
        nged: NormalGraphicalElementData = uri.tag
        self._bitmapsGfx[nged.gfxId] = pixmap

    def onLoadComplete(self, event, total, completed):
        pass

    def onloadError(self, event, uri, errorMsg, errorCode):
        error = f"Load of resource at uri: {uri} failed with err[{errorCode}] {errorMsg}"
        self.error_dialog.showMessage(error)
        QApplication.instance().quit()

    def onElementsLoaded(self, event, uri, resourceType, resource):
        for nged in MapDisplayManager().dataMap.computeGfxList(False, layersFilter=[]):
            if nged.gfxId:
                uri = self.getGfxUri(nged.gfxId)
                uri.tag = nged
                self.gfx_loader.load(uri)

    def loadElementsFile(self) -> None:
        AdapterFactory.addAdapter("ele", ElementsAdapter)
        elementsIndexPath = LangManager().getEntry("config.atouin.path.elements")
        elementsLoader = ResourceLoaderFactory.getLoader(ResourceLoaderType.SINGLE_LOADER)
        elementsLoader.on(ResourceEvent.ERROR, self.onloadError)
        elementsLoader.on(ResourceEvent.LOADED, self.onElementsLoaded)
        elementsLoader.load(Uri(elementsIndexPath))

    def render(dataContainer: DataMapContainer):
        pass

    def makeMap(self):
        layerId = 0
        cellDisabled = False
        hideFg = False
        groundOnly = False
        aInteractiveCell = []
        self._screenResolutionOffset = Point()
        self._screenResolutionOffset.x = (self.bitmapSize.x - MainWindow._startWidth) / 2
        self._screenResolutionOffset.y = (self.bitmapSize.y - MainWindow._startHeight) / 2
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
                        cellCtr.x = cellCtr.startX = int(round(cellPnt.x)) * scaleRatio
                        cellCtr.y = cellCtr.startY = int(round(cellPnt.y)) * scaleRatio
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
        bitmapBackgroundColor = (
            self._map.backgroundColor if self._renderBackgroundColor else QColor(0, 0, 0, 0)
        )  # Transparent if not rendering background

        # Create a QPixmap to draw on
        groundPixmap = QPixmap(bitmapFinalWidth, bitmapFinalHeight)
        groundPixmap.fill(Qt.transparent)  # Set transparent first to handle non-rendering of the background

        # Start painting on QPixmap
        painter = QPainter(groundPixmap)
        if self._renderBackgroundColor:
            painter.fillRect(0, 0, bitmapFinalWidth, bitmapFinalHeight, bitmapBackgroundColor)

        # Assuming renderFixture is another method adapted to handle PyQt
        self._groundPixmapItem = QGraphicsPixmapItem(groundPixmap)
        self._groundPixmapItem.setData(0, "ground")  # Set name equivalent in Qt
        painter.end()
        self.renderFixture(self._map.backgroundFixtures, self._groundBitmap)

    def renderFixture(self, fixtures: list[Fixture], container):
        if not fixtures or not self._renderFixture:
            return

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
                m.rotate(fixture.rotation)
                m.translate(fixture.offsetX + halfWidth, fixture.offsetY + halfHeight)
                # Apply additional offsets
                m.translate(self._screenResolutionOffset.x(), self._screenResolutionOffset.y())

                # Color transformations and rendering
                if fixture.redMultiplier or fixture.greenMultiplier or fixture.blueMultiplier or fixture.alpha != 255:
                    # Adjust painter settings for color
                    color = QColor(
                        255 * fixture.redMultiplier,
                        255 * fixture.greenMultiplier,
                        255 * fixture.blueMultiplier,
                        fixture.alpha,
                    )
                    painter.setPen(color)
                    painter.setBrush(color)

                painter.setTransform(m, combine=False)
                painter.drawPixmap(0, 0, bmpdt)
                painter.end()
