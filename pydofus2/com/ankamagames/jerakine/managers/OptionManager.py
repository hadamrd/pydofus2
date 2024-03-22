import collections

from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import \
    StoreDataManager
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.DataStoreEnum import \
    DataStoreEnum

_optionsManager = {}


class OptionManager:

    def __init__(self, customName=None):
        super().__init__()

        self._defaultValue = collections.defaultdict()
        self._properties = collections.defaultdict()
        self._useCache = collections.defaultdict()
        self._allOptions = []

        self._customName = customName if customName else self.__class__.__name__

        if self._customName in _optionsManager:
            raise ValueError(f"{self._customName} is already used by another option manager.")

        _optionsManager[self._customName] = self
        self._dataStore = DataStoreType(self._customName, True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_ACCOUNT)

    @staticmethod
    def getOptionManager(name):
        return _optionsManager.get(name)

    @staticmethod
    def getOptionManagers():
        return list(_optionsManager.keys())

    @staticmethod
    def reset():
        global _optionsManager
        _optionsManager = {}

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
        return self._properties.get(name)

    def allOptions(self):
        return self._allOptions

    def setOption(self, name, value):
        if name in self._useCache:
            self._properties[name]
            self._properties[name] = value
            if self._useCache[name] and not isinstance(value, QObject):
                StoreDataManager().setData(self._dataStore, name, value)
