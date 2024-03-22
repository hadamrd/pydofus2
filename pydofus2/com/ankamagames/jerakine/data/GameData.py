import os
from typing import TYPE_CHECKING, Any

from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.data.GameDataClassDefinition import GameDataClassDefinition
    from pydofus2.com.ankamagames.jerakine.data.GameDataProcess import GameDataProcess

import threading

from pydofus2.com.ankamagames.jerakine.data.ModuleReader import ModuleReader
from pydofus2.com.ankamagames.jerakine.metaclasses.ThreadSharedSingleton import \
    ThreadSharedSingleton

lock = threading.Lock()


class GameData(metaclass=ThreadSharedSingleton):
    
    def __init__(self) -> None:
        self._modules = dict[str, ModuleReader]()

    def addModule(self, file: str, name: str) -> None:
        self._modules[name] = ModuleReader(file, name=name)

    def addModuleByName(self, moduleName: str) -> None:
        if moduleName not in self._modules:
            common_dir = XmlConfig().getEntry("config.data.path.common")
            file_path = os.path.join(common_dir, f"{moduleName}.d2o")
            self.addModule(file_path, moduleName)

    def getModule(self, moduleName: str) -> ModuleReader:
        if moduleName not in self._modules:
            with lock:
                self.addModuleByName(moduleName)
        return self._modules.get(moduleName)

    def getDataProcessor(self, moduleName: str) -> "GameDataProcess":
        return self.getModule(moduleName)._gameDataProcessor

    def getClassDefinition(self, moduleName: str, classId: int) -> "GameDataClassDefinition":
        return self.getModule(moduleName)._classes[classId]

    def getCount(self, moduleName: str) -> int:
        return self.getModule(moduleName)._counter

    def getObject(self, moduleName: str, objectId) -> Any:
        return self.getModule(moduleName).getObject(objectId)

    def getObjects(self, moduleName: str) -> list[object]:
        return self.getModule(moduleName).getObjects()

    def close(self) -> None:
        for module in self._modules:
            self._modules[module].close()
        self._modules = dict[str, ModuleReader]()
