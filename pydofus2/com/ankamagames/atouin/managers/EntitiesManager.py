from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton


class EntitiesManager(metaclass=Singleton):
    RANDOM_ENTITIES_ID_START: float = -1000000

    def __init__(self):
        self._entities = dict[float, "IEntity"]()
        self._entitiesScheduledForDestruction = dict()
        self._currentRandomEntity = self.RANDOM_ENTITIES_ID_START

    def addEntity(self, entityId: float, entity: "IEntity", strata: int = 0) -> None:
        entityId = float(entityId)
        if entityId in self._entities:
            Logger().warn(f"Entity overwriting! Entity {entityId} has been replaced.")
        self._entities[entityId] = entity

    def getEntity(self, entityId: float) -> "IEntity":
        return self._entities.get(float(entityId))

    def getEntityID(self, entity: "IEntity") -> float:
        for i in self._entities:
            if entity == self._entities[i]:
                return float(i)
        return 0

    def removeEntity(self, entityId: float) -> None:
        entityId = float(entityId)
        if entityId in self._entities:
            del self._entities[entityId]
        if entityId in self._entitiesScheduledForDestruction:
            del self._entitiesScheduledForDestruction[entityId]

    def clearEntities(self) -> None:
        entityBuffer: list = []
        for id in self._entities:
            entityBuffer.append(id)
        for entityId in entityBuffer:
            self.removeEntity(entityId)
        self._entities.clear()

    def setEntitiesVisibility(self, visible: bool) -> None:
        entityBuffer: list = []
        for id in self._entities:
            entityBuffer.append(id)
        for entityId in entityBuffer:
            ts = self._entities[entityId]
            ts.visible = visible

    @property
    def entities(self) -> dict[int, "IEntity"]:
        return self._entities

    @property
    def entitiesScheduledForDestruction(self) -> dict[int, "IEntity"]:
        return self._entitiesScheduledForDestruction

    def getFreeEntityId(self) -> float:
        self._currentRandomEntity -= 1
        while self._entities.get(self._currentRandomEntity) is not None:
            self._currentRandomEntity -= 1
        return self._currentRandomEntity

    def getEntityOnCell(self, cellId: int, oClass=None) -> "IEntity":
        useFilter = oClass is not None
        isMultiFilter: bool = useFilter and isinstance(oClass, list)
        for e in self._entities.values():
            if e and e.position and e.position.cellId == cellId:
                if not isMultiFilter:
                    if not useFilter or not isMultiFilter and isinstance(e, oClass):
                        return e
                else:
                    for cls in oClass:
                        if isinstance(e, cls):
                            return e
        return None

    def getEntitiesOnCell(self, cellId: int, oClass=None) -> list[IEntity]:
        useFilter = oClass is not None
        isMultiFilter = useFilter and isinstance(oClass, list)
        result = []
        for e in self._entities.values():
            if e and e.position and int(e.position.cellId) == int(cellId):
                if isMultiFilter and any(isinstance(e, cls) for cls in oClass):
                    result.append(e)
                elif useFilter and isinstance(e, oClass):
                    result.append(e)
                else:
                    result.append(e)
        return result
