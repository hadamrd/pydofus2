import collections

from PyQt5.QtCore import QObject

from pydofus2.com.ankamagames.berilia.managers.EventsHandler import EventsHandler
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import StoreDataManager
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.DataStoreEnum import DataStoreEnum
from pydofus2.com.ankamagames.jerakine.types.events.PropertyChangeEvent import PropertyChangeEvent


class OptionManager(EventsHandler):
    _optionsManager = dict[str, "OptionManager"]()

    def __init__(self, customName=None):
        super().__init__()

        self._defaultValue = collections.defaultdict()
        self._properties = collections.defaultdict()
        self._useCache = collections.defaultdict()
        self._allOptions = []
        self._customName = customName if customName else self.__class__.__name__

        if self._customName in self._optionsManager:
            raise ValueError(f"{self._customName} is already used by another option manager.")

        self._optionsManager[self._customName] = self
        self._dataStore = DataStoreType(
            self._customName, True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_ACCOUNT
        )

    @classmethod
    def getOptionManager(cls, name) -> "OptionManager":
        return cls._optionsManager.get(name)

    @classmethod
    def getOptionManagers(cls):
        return list(cls._optionsManager.keys())

    @classmethod
    def reset(cls):
        cls._optionsManager.clear()

    def add(self, name, value=None, useCache=True):
        if name not in self._allOptions:
            self._allOptions.append(name)
        self._useCache[name] = useCache
        self._defaultValue[name] = value
        if useCache and StoreDataManager().getData(self._dataStore, name) is not None:
            self._properties[name] = StoreDataManager().getData(self._dataStore, name)
        else:
            self._properties[name] = value

    def getDefaultValue(self, name):
        return self._defaultValue.get(name)

    def restoreDefaultValue(self, name):
        if name in self._useCache:
            self.setOption(name, self._defaultValue[name])

    def getOption(self, name):
        if name not in self._properties:
            print(self._properties)
        return self._properties.get(name)

    def allOptions(self):
        return self._allOptions

    def setOption(self, name, value):
        if name in self._useCache:
            oldValue = self._properties[name]
            self._properties[name] = value
            if self._useCache[name] and not isinstance(value, QObject):
                StoreDataManager().setData(self._dataStore, name, value)
            self.send(PropertyChangeEvent.PROPERTY_CHANGED, name, value, oldValue)
