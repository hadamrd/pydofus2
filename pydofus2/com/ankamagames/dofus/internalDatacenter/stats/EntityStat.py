from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.Stat import Stat


class EntityStat(Stat):
    def __init__(self, id, total_value):
        super().__init__(id, total_value)
        self._entityId = None  # NaN in ActionScript, None in Python for uninitialized value

    @property
    def entityId(self):
        return self._entityId

    @entityId.setter
    def entityId(self, entityId):
        self._entityId = entityId

    def getFormattedMessage(self, message):
        class_name = self.__class__.__qualname__
        return f"{class_name} {self._name} (Entity ID: {self._entityId}, ID: {self._id}): {message}"
