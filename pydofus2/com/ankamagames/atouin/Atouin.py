from PyQt5.QtCore import QRect

from DofusUI.Sprite import Sprite
from DofusUI.StageShareManager import StageShareManager
from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import ElementsAdapter
from pydofus2.com.ankamagames.atouin.resources.adapters.MapsAdapter import MapsAdapter
from pydofus2.com.ankamagames.atouin.rtypes.AtouinOptions import AtouinOptions
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import AdapterFactory
from pydofus2.com.ankamagames.jerakine.types.events.PropertyChangeEvent import PropertyChangeEvent


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

    def setDisplayOptions(self, ao: AtouinOptions):
        self._aoOptions = ao
        self._worldContainer = ao.container
        self._handler = ao.handler
        self._aoOptions.addEventListener(PropertyChangeEvent.PROPERTY_CHANGED, self.onPropertyChange)
        for i in range(self._worldContainer.numChildren):
            self._worldContainer.removeChildAt(i)
        self._overlayContainer = Sprite()
        self._spMapContainer = Sprite()
        self._spChgMapContainer = Sprite()
        self._spGfxContainer = Sprite()
        self._worldMask = Sprite()
        self._worldContainer.mouseEnabled = False
        self._spMapContainer.addEventListener(MouseEvent.ROLL_OUT, self.onRollOutMapContainer)
        self._spMapContainer.addEventListener(MouseEvent.ROLL_OVER, self.onRollOverMapContainer)
        self._spMapContainer.tabChildren = False
        self._spMapContainer.mouseEnabled = False
        self._spChgMapContainer.tabChildren = False
        self._spChgMapContainer.mouseEnabled = False
        self._spGfxContainer.tabChildren = False
        self._spGfxContainer.mouseEnabled = False
        self._spGfxContainer.mouseChildren = False
        self._overlayContainer.tabChildren = False
        self._overlayContainer.mouseEnabled = False
        self._worldMask.mouseEnabled = False
        self._worldContainer.addChild(self._spMapContainer)
        self._worldContainer.addChild(self._spChgMapContainer)
        self._worldContainer.addChild(self._worldMask)
        self._worldContainer.addChild(self._spGfxContainer)
        self._worldContainer.addChild(self._overlayContainer)
        FrustumManager().init(self._spChgMapContainer)
        self._worldContainer.name = "worldContainer"
        self._spMapContainer.name = "mapContainer"
        self._worldMask.name = "worldMask"
        self._spChgMapContainer.name = "chgMapContainer"
        self._spGfxContainer.name = "gfxContainer"
        self._overlayContainer.name = "overlayContainer"
        self.computeWideScreenBitmapWidth(ao.getOption("frustum"))
        self.setWorldMaskDimensions(AtouinConstants.WIDESCREEN_BITMAP_WIDTH)
        hideBlackBorderValue = self._aoOptions.getOption("hideBlackBorder")
        if not hideBlackBorderValue:
            self.setWorldMaskDimensions(StageShareManager.startWidth, 0, 0, 1, "blackBorder")
            self.getWorldMask("blackBorder", False).mouseEnabled = True
        else:
            m = self.getWorldMask("blackBorder", False)
            if m:
                m.parent.removeChild(m)
        self.setFrustrum(ao.getOption("frustum"))
        self.init()

    def onPropertyChange(self, e: PropertyChangeEvent):
        if e.propertyName == "hideBlackBorder":
            if not e.propertyValue:
                self.setWorldMaskDimensions(StageShareManager.startWidth, 0, 0, 1, "blackBorder")
                self.getWorldMask("blackBorder", False).mouseEnabled = True
            else:
                m = self.getWorldMask("blackBorder", False)
                if m:
                    m.parent.removeChild(m)

    def computeWideScreenBitmapWidth(self, frustum):
        RIGHT_GAME_MARGIN = int((AtouinConstants.ADJACENT_CELL_LEFT_MARGIN - 1) * AtouinConstants.CELL_WIDTH)
        LEFT_GAME_MARGIN = int((AtouinConstants.ADJACENT_CELL_RIGHT_MARGIN - 1) * AtouinConstants.CELL_WIDTH)
        MAP_IMAGE_WIDTH = AtouinConstants.CELL_WIDTH * AtouinConstants.MAP_WIDTH + AtouinConstants.CELL_WIDTH
        AtouinConstants.WIDESCREEN_BITMAP_WIDTH = MAP_IMAGE_WIDTH + RIGHT_GAME_MARGIN + LEFT_GAME_MARGIN
        StageShareManager.stageLogicalBounds = QRect(
            -(AtouinConstants.WIDESCREEN_BITMAP_WIDTH - StageShareManager.startWidth) / 2,
            0,
            AtouinConstants.WIDESCREEN_BITMAP_WIDTH,
            StageShareManager.startHeight,
        )
