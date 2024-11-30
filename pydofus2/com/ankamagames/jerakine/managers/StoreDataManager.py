import base64
import sys
from typing import Any

from pydofus2.com.ankamagames.jerakine import JerakineConstants
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.ThreadSharedSingleton import ThreadSharedSingleton
from pydofus2.com.ankamagames.jerakine.types.CustomSharedObject import CustomSharedObject
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.DataStoreEnum import DataStoreEnum


class IExternalizable:
    pass


class Secure:
    pass


class StoreDataManager(metaclass=ThreadSharedSingleton):
    def __init__(self) -> None:
        self._aData = dict()
        self._bStoreSequence: bool = False
        self._nCurrentSequenceNum: int = 0
        self._aStoreSequence: list = []
        self._aSharedObjectCache: dict = {}
        self._aRegisteredClassAlias: dict = {}
        self._bStoreSequence = False
        self._aRegisteredClassAlias = dict()
        self._self = None
        aClass = self.getData(JerakineConstants.DATASTORE_CLASS_ALIAS, "classAliasList")
        if aClass is not None:
            for s in aClass:
                className = base64.b64decode(s).decode()
                try:
                    oClass = getattr(sys.modules[__package__], className)
                    globals().update({aClass[s]: oClass})
                except Exception as e:
                    pass
                self._aRegisteredClassAlias[className] = True

    def getSharedObject(self, sName: str) -> "CustomSharedObject":
        if sName in self._aSharedObjectCache:
            return self._aSharedObjectCache[sName]
        so = CustomSharedObject.getLocal(sName)
        self._aSharedObjectCache[sName] = so
        return so

    def getData(self, dataType: DataStoreType, sKey: str) -> Any:
        if dataType.persistent:
            if dataType.location == DataStoreEnum.LOCATION_LOCAL:
                so = self.getSharedObject(dataType.category)
                if so.data:
                    return so.data.get(sKey)
            elif dataType.location == DataStoreEnum.LOCATION_SERVER:
                pass
            return None
        if dataType.category in self._aData:
            return self._aData[dataType.category][sKey]
        return None

    def isComplexType(self, o) -> bool:
        if type(o) in [int, float, bool, list, str, None.__class__]:
            return False
        else:
            return True

    def registerClass(self, oInstance: type, deepClassScan: bool = False, keepClassInSo: bool = True) -> None:
        if isinstance(oInstance, IExternalizable):
            raise Exception("Can't store a customized IExternalizable in a shared object.")
        if isinstance(oInstance, Secure):
            raise Exception("Can't store a Secure class")
        if self.isComplexType(oInstance):
            className = oInstance.__class__.__qualname__
            if className in self._aRegisteredClassAlias:
                return
            sAlias = className.__hash__()
            Logger().debug("Register " + className + " with alias " + str(sAlias))
            try:
                oClass = oInstance.__class__
                globals().update({sAlias: oClass})
                Logger().warn("Register " + className)
            except Exception as e:
                Logger().error(e)
                self._aRegisteredClassAlias[className] = True
                Logger().fatal("Unable to find the class " + className + " in the current application domain")
                return
            self._aRegisteredClassAlias[className] = True
            if keepClassInSo:
                aClassAlias = self.getSetData(JerakineConstants.DATASTORE_CLASS_ALIAS, "classAliasList", {})
                encoded_class_name = base64.b64encode(className.encode("utf-8")).decode("utf-8")
                aClassAlias[encoded_class_name] = sAlias
                self.setData(
                    JerakineConstants.DATASTORE_CLASS_ALIAS,
                    "classAliasList",
                    aClassAlias,
                )
        if deepClassScan:
            if isinstance(oInstance, dict) or isinstance(oInstance, list):
                desc = oInstance
                if isinstance(oInstance, list[Any]):
                    tmp = oInstance.__class__.__name__
                    leftBracePos = tmp.find("[")
                    tmp = tmp[leftBracePos + 1 : str(reversed(tmp)).find("]") - leftBracePos - 1]
                    self.registerClass(oInstance.__class__(), True, keepClassInSo)
            else:
                desc = self.scanType(oInstance)
            for key in desc:
                if self.isComplexType(oInstance[key]):
                    self.registerClass(oInstance[key], True)
                if desc == oInstance:
                    break

    def setData(self, dataType: DataStoreType, sKey: str, oValue, deepClassScan=False) -> bool:
        if dataType.category not in self._aData:
            self._aData[dataType.category] = dict()
        self._aData[dataType.category][sKey] = oValue
        if dataType.persistent:
            if dataType.location == DataStoreEnum.LOCATION_LOCAL:
                self.registerClass(oValue, deepClassScan)
                so = self.getSharedObject(dataType.category)
                if not so.data:
                    so.data = {}
                so.data[sKey] = oValue
                if not self._bStoreSequence:
                    if not so.flush():
                        return False
                else:
                    self._aStoreSequence[dataType.category] = dataType
                return True
            if dataType.location == DataStoreEnum.LOCATION_SERVER:
                return False
        return True

    def getKeys(self, dataType: DataStoreType) -> list:
        result: list = []
        if dataType.persistent:
            if dataType.location == DataStoreEnum.LOCATION_LOCAL:
                so = self.getSharedObject(dataType.category)
                data = so.data
            if dataType.location == DataStoreEnum.LOCATION_SERVER:
                pass
        elif dataType.category in self._aData:
            data = self._aData[dataType.category]
        if data:
            for key in data:
                result.append(key)
        return result

    def getSetData(self, dataType: DataStoreType, sKey: str, oValue) -> Any:
        o = self.getData(dataType, sKey)
        if o is not None:
            return o
        self.setData(dataType, sKey, oValue)
        return oValue

    def clear(self, dataType: DataStoreType) -> None:
        self._aData = []
        so: CustomSharedObject = self.getSharedObject(dataType.category)
        so.clear()

    def reset(self) -> None:
        s: CustomSharedObject = None
        for s in self._aSharedObjectCache:
            try:
                s.clear()
                s.close()
            except Exception as e:
                pass
        self._aSharedObjectCache = []

    def close(self, dataType: DataStoreType) -> None:
        if dataType.location == DataStoreEnum.LOCATION_LOCAL:
            self._aSharedObjectCache[dataType.category].close()
            del self._aSharedObjectCache[dataType.category]

    def isComplexTypeFromstr(self, name: str) -> bool:
        if name in ("int", "float", "str", "bool", "list", "float", None):
            return False
        else:
            return self._aRegisteredClassAlias[name]

    def scanType(self, obj) -> object:
        name: str = None
        desc: list[str] = DescribeTypeCache.getVariables(obj, False, True, True, True)
        result = {}
        for name in desc:
            if self.isComplexTypeFromstr(obj[name].__class__.__name__):
                result[name] = True
        return result
