from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.Frustum import Frustum
from pydofus2.com.ankamagames.atouin.FrustumManager import FrustumManager
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import ElementsAdapter
from pydofus2.com.ankamagames.atouin.resources.adapters.MapsAdapter import MapsAdapter
from pydofus2.com.ankamagames.atouin.types.AtouinOptions import AtouinOptions
from pydofus2.com.ankamagames.atouin.types.SimpleGraphicsContainer import SimpleGraphicsContainer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import AdapterFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderFactory import ResourceLoaderFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import ResourceLoaderType
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.DofusUI.StageShareManager import StageShareManager


class Atouin(metaclass=Singleton):
    DEFAULT_MAP_EXTENSION = "png"

    def __init__(self):
        self._worldContainer = None
        self._overlayContainer = None
        self._spMapContainer = None
        self._spGfxContainer = None
        self._spChgMapContainer = None
        self._worldMask = None
        self._currentZoom = 1
        self._zoomPosX = 0
        self._zoomPosY = 0
        self._movementListeners = []
        self._aSprites = []
        self._worldVisible = True
        self._aoOptions = None
        AdapterFactory.addAdapter("ele", ElementsAdapter)
        AdapterFactory.addAdapter("dlm", MapsAdapter)

    @property
    def options(self):
        return self._aoOptions

    @options.setter
    def options(self, val):
        self._aoOptions = val

    def setDisplayOptions(self, ao: AtouinOptions):
        self._aoOptions = ao
        self._worldContainer = ao.container
        self._handler = ao.handler
        self._aoOptions.propertyChanged.connect(self.onPropertyChange)

        for item in self._worldContainer.childItems():
            item.setParentItem(None)
            del item

        self._overlayContainer = SimpleGraphicsContainer()
        self._spMapContainer = SimpleGraphicsContainer()
        self._spChgMapContainer = SimpleGraphicsContainer()
        self._spGfxContainer = SimpleGraphicsContainer()
        self._worldMask = SimpleGraphicsContainer()

        self._worldContainer.addChild(self._spMapContainer)
        self._worldContainer.addChild(self._spChgMapContainer)
        self._worldContainer.addChild(self._spGfxContainer)
        self._worldContainer.addChild(self._overlayContainer)
        frustum = ao.getOption("frustum")
        FrustumManager().init(self._spChgMapContainer)
        self.computeWideScreenBitmapWidth(frustum)
        self.setFrustum(frustum)
        self.init()

    def setWorldMask(self):
        self._worldContainer.addChild(self._worldMask)
        self.setWorldMaskDimensions(AtouinConstants.WIDESCREEN_BITMAP_WIDTH)
        hideBlackBorderValue = self._aoOptions.getOption("hideBlackBorder")
        if not hideBlackBorderValue:
            self.setWorldMaskDimensions(StageShareManager().startWidth, 0, 0, 1, "blackBorder")
        else:
            m = self.getWorldMask("blackBorder", False)
            if m:
                self._worldMask.addChild(m)

    def init(self):
        self._aSprites = []
        if not Elements().parsed:
            self.loadElementsFile()

    def loadElementsFile(self):
        elementsLoader = ResourceLoaderFactory.getLoader(ResourceLoaderType.SINGLE_LOADER)
        elementsLoader.loadFailed.connect(self.onElementsError)
        elementsLoader.resourceLoaded.connect(self.onElementsLoaded)
        elementsIndexPath = self.options.getOption("elementsIndexPath")
        elementsLoader.load(Uri(elementsIndexPath))

    def onElementsLoaded(self, uri: Uri, resourceType, elements: Elements):
        Logger().debug("Elements data loaded")

    def onElementsError(self, uri, errorMsg, errorCode):
        Logger().error("Atouin was unable to retrieve the elements directory (" + errorMsg + ")")

    def setFrustum(self, f: Frustum):
        if not self._aoOptions:
            return

        self._aoOptions.setOption("frustum", f)

        # Set scale and position for worldContainer
        self.worldContainer.setScale(f.scale)
        self.worldContainer.setPos(f.x, f.y)

        # Set scale and position for gfxContainer
        self.gfxContainer.setScale(f.scale)
        self.gfxContainer.setPos(f.x, f.y)

        # Set scale and position for overlayContainer
        self.overlayContainer.setScale(f.scale)
        self.overlayContainer.setPos(f.x, f.y)

        # If FrustumManager is a singleton and handles a frustum, ensure it is updated
        FrustumManager().frustum = f

    def setWorldMaskDimensions(self, width, height=0, color=0, alpha=1, name="default"):
        m = self.getWorldMask(name)
        if m:
            color = QColor(color)
            color.setAlphaF(alpha)
            bruch = QBrush(color)
            w = int(width)
            h = StageShareManager().startHeight - height
            x = StageShareManager().startWidth - w
            if x:
                x /= 2
            large_rect = QGraphicsRectItem(QRectF(-2000, -2000, 4000 + w, 4000 + h))
            small_rect = QGraphicsRectItem(QRectF(x, 0, w, h))
            large_rect.setBrush(bruch)
            small_rect.setBrush(bruch)
            large_rect.setParentItem(m)
            small_rect.setParentItem(m)

    def getWorldMask(self, name, createIfNeeded=True):
        for item in self._worldMask.childItems():
            if hasattr(item, "name") and item.name == name:
                return item

        if createIfNeeded:
            m = QGraphicsItem()
            m.setParentItem(self._worldMask)
            m.name = name
            return m

        return None

    def cancelZoom(self):
        Logger().warning("Atouin cancelZoom function not implemented")

    def applyMapZoomScale(self, gameMap):
        Logger().warning("Atouin applyMapZoomScale function not implemented")

    def onPropertyChange(self, propertyName, propertyValue, oldPropertyValue):
        if propertyName == "hideBlackBorder":
            if not propertyValue:
                self.setWorldMaskDimensions(StageShareManager().startWidth, 0, 0, 1, "blackBorder")
            else:
                m = self.getWorldMask("blackBorder", False)
                if m:
                    m.setParentItem(None)

    def computeWideScreenBitmapWidth(self, frustum):
        RIGHT_GAME_MARGIN = int((AtouinConstants.ADJACENT_CELL_LEFT_MARGIN - 1) * AtouinConstants.CELL_WIDTH)
        LEFT_GAME_MARGIN = int((AtouinConstants.ADJACENT_CELL_RIGHT_MARGIN - 1) * AtouinConstants.CELL_WIDTH)
        MAP_IMAGE_WIDTH = AtouinConstants.CELL_WIDTH * AtouinConstants.MAP_WIDTH + AtouinConstants.CELL_WIDTH
        AtouinConstants.WIDESCREEN_BITMAP_WIDTH = MAP_IMAGE_WIDTH + RIGHT_GAME_MARGIN + LEFT_GAME_MARGIN
        StageShareManager().stageLogicalBounds = QRect(
            -(AtouinConstants.WIDESCREEN_BITMAP_WIDTH - StageShareManager().startWidth) / 2,
            0,
            AtouinConstants.WIDESCREEN_BITMAP_WIDTH,
            StageShareManager().startHeight,
        )
        # StageShareManager().stage.setSceneRect(*StageShareManager().stageLogicalBounds.getRect())

    @property
    def chgMapContainer(self) -> SimpleGraphicsContainer:
        return self._spChgMapContainer

    @property
    def gfxContainer(self) -> SimpleGraphicsContainer:
        return self._spGfxContainer

    @property
    def overlayContainer(self) -> SimpleGraphicsContainer:
        return self._overlayContainer

    @property
    def worldMask(self) -> SimpleGraphicsContainer:
        return self._worldMask

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, value):
        self._handler = value

    @property
    def options(self):
        return self._aoOptions

    @options.setter
    def options(self, options):
        self._aoOptions = options

    @property
    def currentZoom(self):
        return self._currentZoom

    @currentZoom.setter
    def currentZoom(self, value):
        self._currentZoom = value

    @property
    def cellOverEnabled(self):
        return InteractiveCellManager().cellOverEnabled

    @cellOverEnabled.setter
    def cellOverEnabled(self, value):
        InteractiveCellManager().cellOverEnabled = value

    @property
    def rootContainer(self):
        return self._worldContainer

    @property
    def worldIsVisible(self):
        return self._worldContainer.isVisible()

    @property
    def worldContainer(self):
        return self._spMapContainer
