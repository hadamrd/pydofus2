from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import ElementsAdapter
from pydofus2.com.ankamagames.atouin.resources.adapters.MapsAdapter import MapsAdapter
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import AdapterFactory


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

    def setDisplayOptions(self, ao):
        pass

    def onPropertyChange(self):
        pass

    def computeWideScreenBitmapWidth(self, frustum):
        RIGHT_GAME_MARGIN = int((AtouinConstants.ADJACENT_CELL_LEFT_MARGIN - 1) * AtouinConstants.CELL_WIDTH)
        LEFT_GAME_MARGIN = int((AtouinConstants.ADJACENT_CELL_RIGHT_MARGIN - 1) * AtouinConstants.CELL_WIDTH)
        MAP_IMAGE_WIDTH = AtouinConstants.CELL_WIDTH * AtouinConstants.MAP_WIDTH + AtouinConstants.CELL_WIDTH
        AtouinConstants.WIDESCREEN_BITMAP_WIDTH = MAP_IMAGE_WIDTH + RIGHT_GAME_MARGIN + LEFT_GAME_MARGIN
