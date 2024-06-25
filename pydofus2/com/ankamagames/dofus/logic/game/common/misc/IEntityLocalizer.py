from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity


class IEntityLocalizer:
    def getEntity(self, param1: float) -> IEntity:
        raise NotImplementedError()

    def unregistered(self) -> None:
        raise NotImplementedError()
