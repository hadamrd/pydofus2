import io
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QErrorMessage, QGraphicsPixmapItem,
                             QGraphicsScene, QGraphicsView, QMainWindow)

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import \
    NormalGraphicalElementData
from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import \
    MapDisplayManager
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import \
    ElementsAdapter
from pydofus2.com.ankamagames.jerakine.data.I18nFileAccessor import \
    I18nFileAccessor
from pydofus2.com.ankamagames.jerakine.managers.LangManager import LangManager
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import \
    AdapterFactory
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import \
    ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderFactory import \
    ResourceLoaderFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import \
    ResourceLoaderType
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri

I18nFileAccessor() #This will load the i18n files don't forget to do it
GFX_PATH = LangManager().getEntry("config.gfx.path.cellElement")

class MainWindow(QMainWindow):
    _startWidth = 1280
    _startHeight = 1024
    
    def __init__(self, mapId, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setObjectName("sharedStage")
        self.setWindowTitle('Map Renderer')
        self.stage = QGraphicsView(self)
        self.worldContainer = MapRenderer(mapId, self)        
        self.stage.setScene(self.worldContainer)
        self.stage.setGeometry(0, 0, self._startWidth, self._startHeight)
        self.stage.setObjectName("stage")
        MAP_IMAGE_WIDTH = AtouinConstants.CELL_WIDTH * AtouinConstants.MAP_WIDTH + AtouinConstants.CELL_WIDTH
        AtouinConstants.WIDESCREEN_BITMAP_WIDTH = MAP_IMAGE_WIDTH
        self.worldContainer.setSceneRect(0, 0, AtouinConstants.WIDESCREEN_BITMAP_WIDTH, MainWindow._startHeight)
        self.setCentralWidget(self.stage)
        QTimer.singleShot(0, self.worldContainer.loadElementsFile)
        self.show()

class MapRenderer(QGraphicsScene):
    
    def __init__(self, mapId, parent) -> None:
        super(MapRenderer, self).__init__(parent)
        MapDisplayManager().loadMap(mapId)
        self.error_dialog = QErrorMessage(parent)
        self.gfx_loader = ResourceLoaderFactory.getLoader(
            ResourceLoaderType.PARALLEL_LOADER
        )
        self.gfx_loader.on(ResourceEvent.ERROR, self.onloadError)
        self.gfx_loader.on(ResourceEvent.LOADED, self.onGfxsLoaded)
        self.gfx_loader.on(ResourceEvent.LOADER_COMPLETE, self.onLoadComplete)
        self.gfx_loader.on(ResourceEvent.LOADER_PROGRESS, self.onMapLoadingProgress)
        self.mousePressEvent = self.onSceneMousePress
        self.elemCount = 0

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
        
    def getGfxUri(self, gfxId) -> Uri:
        isJpg = Elements().isJpg(gfxId)
        path_str = (
            GFX_PATH
            + "/"
            + ("jpg" if isJpg else "png")
            + "/"
            + str(gfxId)
            + "."
            + ("jpg" if isJpg else "png")
        )
        return Uri(path_str, gfxId)
    
    def onGfxsLoaded(self, event, uri: Uri, resourceType, image_bytes: io.BytesIO):
        grid_columns = 10  # Number of columns in the grid
        witem_size = 1.5 * AtouinConstants.CELL_WIDTH  # Size of each item in the grid
        hitem_size = 1.5 * AtouinConstants.CELL_HEIGHT
        margin = 20  # Margin between items
        
            
        pixmap = QPixmap()
        pixmap.loadFromData(image_bytes)
        nged: NormalGraphicalElementData = uri.tag
        cellId = MapDisplayManager().dataMap.getGfxCell(nged.gfxId)
        
        Cell.cellPixelCoords(cellId)
        
        pixmapItem = QGraphicsPixmapItem(pixmap)  # Create QGraphicsPixmapItem
        pixmapItem.setToolTip(str(nged.gfxId))
        
        # Calculate position in the grid
        row = self.elemCount // grid_columns
        col = self.elemCount % grid_columns
        
        # Calculate position of the item
        x = col * (witem_size + margin)
        y = row * (hitem_size + margin)
        pixmapItem.setPos(x, y)
        
        # pixmapItem.setPos(imageCenter.x - nged.origin.x + nged.size.x, imageCenter.y - nged.origin.y + nged.size.y)
        pixmapItem.setScale(min(witem_size / pixmap.width(), hitem_size / pixmap.height()))
        pixmapItem.setVisible(True)
        self.elemCount += 1

        self.addItem(pixmapItem)  # Add item to scene
        
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
        elementsLoader = ResourceLoaderFactory.getLoader(
            ResourceLoaderType.SINGLE_LOADER
        )
        elementsLoader.on(ResourceEvent.ERROR, self.onloadError)
        elementsLoader.on(ResourceEvent.LOADED, self.onElementsLoaded)
        elementsLoader.load(Uri(elementsIndexPath))

if __name__ == "__main__":
    mapId = 154010883
    app = QApplication(sys.argv)
    main_window = MainWindow(mapId)
    sys.exit(app.exec_())
