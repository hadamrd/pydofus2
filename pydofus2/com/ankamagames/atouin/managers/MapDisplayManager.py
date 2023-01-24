# from pydofus2.com.ankamagames.atouin.managers.InteractiveCellManager import (
#     InteractiveCellManager,
# )
from pydofus2.com.ankamagames.atouin.data.map.Layer import Layer
from pydofus2.com.ankamagames.atouin.enums.ElementTypesEnum import ElementTypesEnum
from pydofus2.com.ankamagames.atouin.messages.MapLoadedMessage import MapLoadedMessage
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from time import perf_counter
import pydofus2.com.ankamagames.atouin.utils.DataMapProvider as dmpm
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.resources.loaders.MapLoader import MapLoader
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.positions.WorldPoint import WorldPoint

logger = Logger("Dofus2")


class MapDisplayManager(metaclass=Singleton):
    
    def __init__(self) -> None:
        self._currentMapRendered = True
        self._currentMap = None
        self.currentDataMap = None
        self._lastMap: WorldPoint = None
        self._nMapLoadStart = 0
        self._nMapLoadEnd = 0
        self._forceReloadWithoutCache = False
        self._identifiedElementPosition = dict[int, MapPoint]()

    @property
    def dataMap(self):
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
        self._identifiedElementPosition = dict()
        for layer in self.dataMap.layers:
            if layer.layerId == Layer.LAYER_GROUND:
                continue
            for cell in layer.cells:
                for element in cell.elements:
                    if element.elementType == ElementTypesEnum.GRAPHICAL:
                        if element.identifier > 0:
                            self._identifiedElementPosition[element.identifier] = MapPoint.fromCellId(cell.cellId)

    def isIdentifiedElement(self, identifier: int) -> bool:
        return self._identifiedElementPosition.get(identifier)

    def getIdentifiedElementPosition(self, identifier: int) -> MapPoint:
        return self._identifiedElementPosition.get(identifier)

    def mapDisplayed(self) -> None:
        pass

    def loadMap(self, mapId: int, forceReloadWithoutCache: bool = False, decryptionKey=None) -> None:
        from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
        self.currentDataMap = None
        self._forceReloadWithoutCache = forceReloadWithoutCache
        self._currentMapRendered = False
        self._nMapLoadStart = perf_counter()
        map = MapLoader.load(mapId, key=decryptionKey)
        self._currentMapRendered = True
        self._nMapLoadEnd = perf_counter()
        logger.debug(f"Map {map.id} loaded in " + str(self._nMapLoadEnd - self._nMapLoadStart) + " seconds")
        dmpm.DataMapProvider().resetUpdatedCell()
        dmpm.DataMapProvider().resetSpecialEffects()
        self.currentDataMap = map
        self._currentMap = WorldPoint.fromMapId(map.id)
        msg = MapLoadedMessage()
        msg.id = self._currentMap.mapId
        self.initIdentifiedElements()
        if Kernel().worker.contains("RoleplayContextFrame"):
            Kernel().worker.getFrame("RoleplayContextFrame").process(msg)
        elif Kernel().worker.contains("FightContextFrame"):
            Kernel().worker.getFrame("FightContextFrame").process(msg)
        else:
            logger.warning("No context frame found!")
