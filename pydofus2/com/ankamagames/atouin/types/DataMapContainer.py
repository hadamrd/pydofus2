from PyQt5.QtWidgets import QGraphicsItem, QGraphicsItemGroup

from pydofus2.com.ankamagames.atouin.Atouin import Atouin
from pydofus2.com.ankamagames.atouin.data.map.Map import Map
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.types.CellReference import CellReference
from pydofus2.com.ankamagames.atouin.types.LayerContainer import LayerContainer
from pydofus2.com.ankamagames.atouin.types.SimpleGraphicsContainer import SimpleGraphicsContainer
from pydofus2.com.ankamagames.atouin.utils.VisibleCellDetection import VisibleCellDetection
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.types.events.PropertyChangeEvent import PropertyChangeEvent
from pydofus2.com.ankamagames.jerakine.types.positions.WorldPoint import WorldPoint


class DataMapContainer:
    interactiveCell = {}
    _animatedElement = []
    _spMap = None

    def __init__(self, mapData: Map):
        self._map = mapData
        self._aLayers = None
        if not self._spMap:
            self._spMap = SimpleGraphicsContainer()
            self._aLayers = {}
        self._aCell = dict[int, CellReference]()
        self._animatedElements = []
        self._alwaysAnimatedElements = {}
        self._allowAnimatedGfx = Atouin().options.getOption("allowAnimatedGfx")
        self._useWorldEntityPool = Atouin().options.getOption("useWorldEntityPool")
        self.layerDepth = []
        self.id = mapData.id
        self.rendered = False
        Atouin().options.on(PropertyChangeEvent.PROPERTY_CHANGED, self.onOptionChange)

    @property
    def dataMap(self):
        return self._map

    def onOptionChange(self, option_name, value):
        if option_name == "allowAnimatedGfx":
            self._allowAnimatedGfx = value
        elif option_name == "useWorldEntityPool":
            self._useWorldEntityPool = value

    def getLayer(self, nId) -> LayerContainer:
        if nId not in self._aLayers:
            self._aLayers[nId] = LayerContainer(nId)
        return self._aLayers[nId]

    def isRegisteredCell(self, nId):
        return self._aCell.get(nId) is not None

    def getCell(self):
        return self._aCell

    def getLayer(self, nId) -> LayerContainer:
        if nId not in self._aLayers:
            self._aLayers[nId] = LayerContainer(nId)  # Assuming LayerContainer exists
        return self._aLayers[nId]

    def getCellReference(self, nId: int) -> CellReference:
        if nId not in self._aCell:
            self._aCell[nId] = CellReference(nId)
        return self._aCell[nId]

    def clean(self, bForceCleaning=False):
        if not bForceCleaning:
            provider = VisibleCellDetection.detectCell(
                False,
                self._map,
                WorldPoint.fromMapId(self.id),
                Atouin().options.getOption("frustum"),
                MapDisplayManager().currentMapPoint,
            ).cell
        else:
            provider = list(range(len(self._aCell)))
        for k in provider:
            cellReference = self._aCell.get(k)
            if cellReference:
                sprites_to_remove = []
                for sprite in cellReference.listSprites:
                    if sprite:
                        parentSprite = sprite.parentItem()
                        if not isinstance(parentSprite, QGraphicsItemGroup):
                            raise Exception("parent sprite must graphics item group!")
                        sprites_to_remove.append(sprite)
                        if not parentSprite.childItems():
                            if not parentSprite.parentItem():
                                raise Exception(
                                    "Cell reference sprite has a parent sprite that does not have a parent"
                                )
                            grandParent = parentSprite.parentItem()
                            if not isinstance(grandParent, QGraphicsItemGroup):
                                raise Exception("Cell reference sprite parent of parent is not a QGraphicsItemGroup")
                            grandParent.removeFromGroup(parentSprite)
                for sprite in sprites_to_remove:
                    parentSprite.removeFromGroup(sprite)
                    cellReference.listSprites.remove(sprite)
                del self._aCell[k]

        p = WorldPoint.fromMapId(self._map.id)
        p.x -= MapDisplayManager().currentMapPoint.x
        p.y -= MapDisplayManager().currentMapPoint.y
        return abs(p.x) > 1 or abs(p.y) > 1

    def mapContainer(self):
        return self._spMap

    @property
    def dataMap(self):
        return self._map

    def addAnimatedElement(self, element, data):
        d = {"element": element, "data": data}
        self._animatedElement.append(d)
        self.updateAnimatedElement(d)

    def setTemporaryAnimatedElementState(self, active):
        self._temporaryEnable = active
        for d in self._animatedElement:
            self.updateAnimatedElement(d)

    def addAlwaysAnimatedElement(self, id):
        for o in self._animatedElement:
            if o["element"].identifier == id:
                self._alwaysAnimatedElement[o] = True
                self.updateAnimatedElement(o)

    def updateAnimatedElement(self, element):
        Logger().warning("DataMapContainer method updateAnimatedElement not implemented yet")

    @property
    def x(self):
        return self._spMap.x()

    @x.setter
    def x(self, value):
        self._spMap.setX(value)

    @property
    def y(self):
        return self._spMap.y()

    @y.setter
    def y(self, value):
        self._spMap.setY(value)

    @property
    def scaleX(self):
        return self._spMap.scale()

    @scaleX.setter
    def scaleX(self, value):
        self._spMap.setScale(value)

    @property
    def scaleY(self):
        return self._spMap.scale()

    @scaleY.setter
    def scaleY(self, value):
        self._spMap.setScale(value)

    def addChild(self, item: QGraphicsItem):
        item.setParentItem(self._spMap)
        return item

    def contains(self, item):
        return item in self._spMap.childItems()

    def getChildByName(self, name):
        for item in self._spMap.childItems():
            if hasattr(item, "name") and item.name == name:
                return item
        return None

    def removeChild(self, item: QGraphicsItem):
        if item.parentItem() == self._spMap:
            item.setParentItem(self._spMap)
        return item
