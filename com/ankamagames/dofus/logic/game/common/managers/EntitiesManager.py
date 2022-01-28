import logging

from com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from com.ankamagames.jerakine.utils.errors.singletonError import SingletonError
logger = logging.getLogger("bot")  


class EntitiesManager:

   RANDOM_ENTITIES_ID_START:float = -1000000
   _entitiesScheduledForDestruction:list = []
   _currentRandomEntity:float = -1000000
   _entities = dict[IEntity]()
   _self = None

   def __init__(self):
      if self._self:
         raise SingletonError("Warning : EntitiesManager is a singleton class and shoulnd\'t be instancied directly!");
      self._entities = []
      self._entitiesScheduledForDestruction = []
      # Atouin.getInstance().options.addEventListener(PropertyChangeEvent.PROPERTY_CHANGED,self.onPropertyChanged);

   @classmethod
   def getInstance(cls) -> 'EntitiesManager': 
      if not cls._self:
         _self = EntitiesManager()
      return _self

   def addAnimatedEntity(self, entityID:float, entity:IEntity, strata:int = 0) -> None:
      if self._entities[entityID] != None:
         logger.warn("Entity overwriting! Entity " + entityID + " has been replaced.")
      self._entities[entityID] = entity

   def getEntity(self, entityID:float) -> IEntity:
      return self._entities[entityID]

   def getEntityID(self, entity:IEntity) -> float:
      i = None
      for i in self._entities:
         if entity == self._entities[i]:
            return float(i)
      return 0

   def removeEntity(self, entityID:float) -> None:
      if self._entities[entityID]:
         del self._entities[entityID]
         if self._entitiesScheduledForDestruction[entityID]:
            del self._entitiesScheduledForDestruction[entityID]

   def clearEntities(self) -> None:
      entityBuffer:list = []
      for id in self._entities:
         entityBuffer.append(id)
      for entityId in entityBuffer:
         self.removeEntity(entityId)
      self._entities = {}

   def setEntitiesVisibility(self, visible:bool) -> None:
      entityBuffer:list = []
      for id in self._entities:
         entityBuffer.append(id)
      for entityId in entityBuffer:
         ts = self._entities[entityId]
         ts.visible = visible

   def entities(self) -> list:
      return self._entities

   def entitiesScheduledForDestruction(self) -> list:
      return self._entitiesScheduledForDestruction

   def entitiesCount(self) -> int:
      count:int = 0
      for _ in self._entities:
         count += 1
      return count

   def getFreeEntityId(self) -> float:
      self._currentRandomEntity -= 1
      while self._entities[self._currentRandomEntity] != None:
         self._currentRandomEntity -= 1
      return self._currentRandomEntity

   def getEntityOnCell(self, cellId:int, oClass = None) -> IEntity:
      useFilter = oClass != None
      isMultiFilter:bool = useFilter and oClass is list
      for e in self._entities:
         if e and e.position and e.position.cellId == cellId:
            if not isMultiFilter:
               if not useFilter or not isMultiFilter and e is oClass:
                  return e
            else:
               for i in range(oClass):
                  if e is oClass[i]:
                     return e
      return None

   def getEntitiesOnCell(self, cellId:int, oClass = None) -> list:
      useFilter = oClass != None
      isMultiFilter:bool = useFilter and oClass is list
      result:list = []
      for e in self._entities:
         if e and e.position and e.position.cellId == cellId:
            if not isMultiFilter:
               if not useFilter or not isMultiFilter and e is oClass:
                  result.append(e)
            else:
               for cls in oClass:
                  if isinstance(e, cls):
                     result.append(e)
                     break
      return result

