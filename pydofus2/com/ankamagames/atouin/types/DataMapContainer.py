from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsItemGroup

from pydofus2.com.ankamagames.atouin.Atouin import Atouin
from pydofus2.com.ankamagames.atouin.data.map.Map import Map


class DataMapContainer:
    propertyChanged = pyqtSignal(str, object)

    def __init__(self, mapData: Map):
        self._map = mapData
        self._spMap = QGraphicsItemGroup()
        self._aLayers = []
        self._aCell = []
        self._interactiveCells = []
        self._animatedElements = []
        self._alwaysAnimatedElements = {}
        self._allowAnimatedGfx = Atouin().options.getOption("allowAnimatedGfx")
        self._useWorldEntityPool = Atouin().options.getOption("useWorldEntityPool")
        self.layerDepth = []
        self.id = mapData.id
        self.rendered = False

        # Connect to the custom signal for property changes if needed
        self.propertyChanged.connect(self.onOptionChange)

    def addLayer(self, layer):
        """Add a layer to the scene."""
        self._layers.append(layer)
        self.scene.addItem(layer)

    def removeLayer(self, layer):
        """Remove a layer from the scene."""
        if layer in self._layers:
            self.scene.removeItem(layer)
            self._layers.remove(layer)

    def onOptionChange(self, option_name, value):
        """Handle changes to options."""
        if option_name == "allowAnimatedGfx":
            self._allowAnimatedGfx = value
        elif option_name == "useWorldEntityPool":
            self._useWorldEntityPool = value

    def clear(self):
        """Clear all items from the scene and reset container states."""
        for item in self.scene.items():
            if isinstance(item, QGraphicsItem):
                self.scene.removeItem(item)
        self._layers.clear()
        self._animatedElements.clear()
        self._alwaysAnimatedElements.clear()
