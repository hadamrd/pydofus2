import threading

from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.IEntityLocalizer import IEntityLocalizer
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton

lock = threading.Lock()


class FightEntitiesHolder(IEntityLocalizer, metaclass=Singleton):
    def __init__(self):
        self._holdedEntities = dict()
        DofusEntities().registerLocalizer(self)
        super().__init__()

    def getEntity(self, entityId: float) -> IEntity:
        return self._holdedEntities.get(entityId)

    def holdEntity(self, entity: IEntity) -> None:
        with lock:
            if entity.id not in self._holdedEntities:
                self._holdedEntities[entity.id] = entity

    def unholdEntity(self, entityId: float) -> None:
        with lock:
            if entityId in self._holdedEntities:
                del self._holdedEntities[entityId]

    def reset(self) -> None:
        with lock:
            self._holdedEntities.clear()

    def getEntities(self) -> dict:
        return self._holdedEntities

    def unregistered(self) -> None:
        with lock:
            self._holdedEntities.clear()
            FightEntitiesHolder.clear()
