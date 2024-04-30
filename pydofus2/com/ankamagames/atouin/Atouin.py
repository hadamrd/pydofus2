from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsRectItem

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.Frustum import Frustum
from pydofus2.com.ankamagames.atouin.FrustumManager import FrustumManager
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import ElementsAdapter
from pydofus2.com.ankamagames.atouin.resources.adapters.MapsAdapter import MapsAdapter
from pydofus2.com.ankamagames.atouin.types.AtouinOptions import AtouinOptions
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import AdapterFactory
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderFactory import ResourceLoaderFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import ResourceLoaderType
from pydofus2.com.ankamagames.jerakine.types.events.PropertyChangeEvent import PropertyChangeEvent
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
        self._aoOptions: AtouinOptions = None

        AdapterFactory.addAdapter("ele", ElementsAdapter)
        AdapterFactory.addAdapter("dlm", MapsAdapter)

    @property
    def options(self):
        return self._aoOptions

    @options.setter
    def options(self, val):
        self._aoOptions = val

    def _setMouseInteraction(self, container: QGraphicsItemGroup, enabled, disable_children=False):
        container.setAcceptHoverEvents(enabled)
        container.setFlag(QGraphicsItem.ItemIsSelectable, enabled)
        container.setFlag(QGraphicsItem.ItemIsMovable, enabled)
        if not enabled:
            container.setFlag(QGraphicsItem.ItemSendsGeometryChanges, enabled)
        if disable_children:
            for item in container.childItems():
                item.setAcceptHoverEvents(enabled)
                item.setFlag(QGraphicsItem.ItemIsSelectable, enabled)
                item.setFlag(QGraphicsItem.ItemIsMovable, enabled)
                item.setFlag(QGraphicsItem.ItemSendsGeometryChanges, enabled)

    def setDisplayOptions(self, ao: AtouinOptions):
        self._aoOptions = ao
        self._worldContainer = ao.container
        self._handler = ao.handler
        self._aoOptions.on(PropertyChangeEvent.PROPERTY_CHANGED, self.onPropertyChange)

        # Remove all children from _worldContainer
        for item in self._worldContainer.childItems():
            self._worldContainer.removeFromGroup(item)

        self._overlayContainer = QGraphicsItemGroup()
        self._spMapContainer = QGraphicsItemGroup()
        self._spChgMapContainer = QGraphicsItemGroup()
        self._spGfxContainer = QGraphicsItemGroup()
        self._worldMask = QGraphicsItemGroup()

        self._setMouseInteraction(self._worldContainer, False)
        self._setMouseInteraction(self._spMapContainer, False)
        self._setMouseInteraction(self._spChgMapContainer, False)
        self._setMouseInteraction(self._spGfxContainer, False, disable_children=True)
        self._setMouseInteraction(self._overlayContainer, False)
        self._setMouseInteraction(self._worldMask, False)

        self._worldContainer.addToGroup(self._spMapContainer)
        self._worldContainer.addToGroup(self._spChgMapContainer)
        # self._worldContainer.addToGroup(self._worldMask)
        self._worldContainer.addToGroup(self._spGfxContainer)
        self._worldContainer.addToGroup(self._overlayContainer)

        FrustumManager().init(self._spChgMapContainer)
        self.computeWideScreenBitmapWidth(ao.getOption("frustum"))
        # self.setWorldMaskDimensions(AtouinConstants.WIDESCREEN_BITMAP_WIDTH)
        # hideBlackBorderValue = self._aoOptions.getOption("hideBlackBorder")
        # if not hideBlackBorderValue:
        #     self.setWorldMaskDimensions(StageShareManager().startWidth, 0, 0, 1, "blackBorder")
        #     # self.getWorldMask("blackBorder", False).mouseEnabled = True TODO
        # else:
        #     m = self.getWorldMask("blackBorder", False)
        #     if m:
        #         self._worldMask.removeFromGroup(m)
        self.setFrustum(ao.getOption("frustum"))
        self.init()

    def init(self):
        self._aSprites = []
        if not Elements().parsed:
            self.loadElementsFile()

    def loadElementsFile(self):
        elementsLoader = ResourceLoaderFactory.getLoader(ResourceLoaderType.SINGLE_LOADER)
        elementsLoader.on(ResourceEvent.ERROR, self.onElementsError, False, 0, True)
        elementsLoader.on(ResourceEvent.LOADED, self.onElementsLoaded)
        elementsLoader.load(Uri(self.options.getOption("elementsIndexPath")))

    def onElementsLoaded(self, event, uri: Uri, resourceType, elements: Elements):
        Logger().debug("Elements data loaded")

    def onElementsError(self, e, uri, errorMsg, errorCode):
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
            m.addToGroup(large_rect)
            m.addToGroup(small_rect)

    def getWorldMask(self, name, createIfNeeded=True):
        for item in self._worldMask.childItems():
            if hasattr(item, "name") and item.name == name:
                return item

        if createIfNeeded:
            m = QGraphicsItemGroup()
            self._worldMask.addToGroup(m)
            m.name = name  # Assign the name
            # Here find some way to disable mouse from this element or maybe its disabled by default
            return m

        return None

    def cancelZoom(self):
        Logger().warning("Atouin cancel zoom function not implemented")

    def onPropertyChange(self, e: PropertyChangeEvent, propertyName, propertyValue, oldPropertyValue):
        if propertyName == "hideBlackBorder":
            if not propertyValue:
                self.setWorldMaskDimensions(StageShareManager().startWidth, 0, 0, 1, "blackBorder")
                self.getWorldMask("blackBorder", False).mouseEnabled = True
            else:
                m = self.getWorldMask("blackBorder", False)
                if m:
                    self._worldContainer.removeFromGroup(m)

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

    @property
    def chgMapContainer(self):
        return self._spChgMapContainer

    @property
    def gfxContainer(self):
        return self._spGfxContainer

    @property
    def overlayContainer(self):
        return self._overlayContainer

    @property
    def worldMask(self):
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
