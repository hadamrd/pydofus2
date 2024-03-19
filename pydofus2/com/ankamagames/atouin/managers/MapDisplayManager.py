from time import perf_counter

import pydofus2.com.ankamagames.atouin.utils.DataMapProvider as dmpm
from pydofus2.com.ankamagames.atouin.data.map.Layer import Layer
from pydofus2.com.ankamagames.atouin.data.map.Map import Map
from pydofus2.com.ankamagames.atouin.enums.ElementTypesEnum import \
    ElementTypesEnum
from pydofus2.com.ankamagames.atouin.messages.MapLoadedMessage import \
    MapLoadedMessage
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.resources.loaders.MapLoader import \
    MapLoader
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.positions.WorldPoint import \
    WorldPoint


class MapDisplayManager(metaclass=Singleton):
    def __init__(self) -> None:
        self._currentMapRendered = True
        self._currentMap = None
        self.currentDataMap: Map = None
        self._lastMap: WorldPoint = None
        self._nMapLoadStart = 0
        self._nMapLoadEnd = 0
        self._forceReloadWithoutCache = False
        self._identifiedElement = dict[int, MapPoint]()

    @property
    def dataMap(self) -> Map:
        return self.currentDataMap

    @property
    def currentMapPoint(self) -> WorldPoint:
        return self._currentMap

    @property
    def mapInstanceId(self) -> float:
        return self._mapInstanceId

    @mapInstanceId.setter
    def mapInstanceId(self, mapId: float) -> None:
        self._mapInstanceId = mapId

    def reset(self) -> None:
        self._currentMap = None
        self._mapInstanceId = 0
        self._currentMapRendered = True
        self._lastMap = None

    def initIdentifiedElements(self):
        self._identifiedElement = dict[int, dict]()
        for layer in self.dataMap.layers:
            if layer.layerId == Layer.LAYER_GROUND:
                continue
            for cell in layer.cells:
                for element in cell.elements:
                    if element.elementType == ElementTypesEnum.GRAPHICAL:
                        if element.identifier > 0:
                            self._identifiedElement[element.identifier] = {
                                "elementId": element.identifier,
                                "typeId": element.elementId,
                                "position": MapPoint.fromCellId(cell.cellId),
                                "elementType": element.elementType
                            }

    def isIdentifiedElement(self, identifier: int) -> bool:
        return self._identifiedElement.get(identifier)

    def getIdentifiedElementPosition(self, identifier: int) -> MapPoint:
        return self._identifiedElement.get(identifier).get("position")
    
    def loadMap(self, mapId: int, forceReloadWithoutCache: bool = False, decryptionKey=None) -> None:
        from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel

        self.currentDataMap = None
        self._forceReloadWithoutCache = forceReloadWithoutCache
        self._currentMapRendered = False
        self._nMapLoadStart = perf_counter()
        self.currentDataMap = MapLoader.load(mapId, key=decryptionKey)
        if self.currentDataMap is None:
            raise Exception(f"Map {mapId} not loaded!")
        self._currentMapRendered = True
        self._nMapLoadEnd = perf_counter()
        Logger().separator(f"Map {self.currentDataMap.id} loaded", "#")
        dmpm.DataMapProvider().resetUpdatedCell()
        dmpm.DataMapProvider().resetSpecialEffects()
        self._currentMap = WorldPoint.fromMapId(self.currentDataMap.id)
        msg = MapLoadedMessage()
        msg.id = self._currentMap.mapId
        self.initIdentifiedElements()
        if Kernel().roleplayContextFrame:
            Kernel().roleplayContextFrame.process(msg)
        elif Kernel().fightContextFrame:
            Kernel().fightContextFrame.process(msg)
        else:
            Logger().warning("No context frame found!")
