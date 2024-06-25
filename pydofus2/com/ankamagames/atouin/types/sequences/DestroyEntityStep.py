from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import EntitiesManager
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class DestroyEntityStep(AbstractSequencable):

    _entity: IEntity

    _waitAnim: bool

    _waitAnimForCallback: bool

    def __init__(self, entity: IEntity, waitAnim: bool = False, waitAnimForCallback: bool = False):
        super().__init__()
        self._entity = entity
        self._waitAnim = waitAnim
        self._waitAnimForCallback = waitAnimForCallback

    def start(self) -> None:
        EntitiesManager().entitiesScheduledForDestruction[self._entity.id] = True
        self.destroyEntity()
        if not self._waitAnimForCallback:
            self.executeCallbacks()

    def addAnimEndListeners(self) -> None:
        pass

    def destroyEntity(self, pEvent) -> None:
        if EntitiesManager().entitiesScheduledForDestruction.get(self._entity.id):
            del self._entity
        if pEvent and self._waitAnimForCallback:
            self.executeCallbacks()
