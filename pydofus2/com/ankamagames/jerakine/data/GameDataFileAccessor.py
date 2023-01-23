from pathlib import Path
from time import perf_counter
from typing import TYPE_CHECKING, Any
from pydofus2.com.ankamagames.dofus import Constants
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.data.GameDataClassDefinition import GameDataClassDefinition
    from pydofus2.com.ankamagames.jerakine.data.GameDataProcess import GameDataProcess
from pydofus2.com.ankamagames.jerakine.data.ModuleReader import ModuleReader
from pydofus2.com.ankamagames.jerakine.metaclasses.ThreadSharedSingleton import ThreadSharedSingleton
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
logger = Logger("Dofus2")
import threading
lock = threading.Lock()
class GameDataFileAccessor(metaclass=ThreadSharedSingleton):
    
    def __init__(self) -> None:
        self._modules = dict[str, ModuleReader]()

    def init(self, file: str) -> None:
        with lock:
            nativeFile = Path(file)
            moduleName: str = nativeFile.name.split(".d2o")[0]
            s = perf_counter()
            self._modules[moduleName] = ModuleReader(nativeFile.open("rb"))
            logger.info(f"Loaded '{nativeFile.name}' module in {perf_counter() - s:.2f}s")

    def initFromModuleName(self, moduleName: str) -> None:
        if moduleName not in self._modules:
            modle_file_path = Constants.DOFUS_COMMON_DIR / f"{moduleName}.d2o"
            self.init(modle_file_path)

    def initFromBinaryStream(self, modulename: str, moduleBinaries: BinaryStream):
        self._modules[modulename] = ModuleReader(moduleBinaries)

    def getDataProcessor(self, moduleName: str) -> "GameDataProcess":
        if moduleName not in self._modules:
            self.initFromModuleName(moduleName)
        return self._modules[moduleName]._gameDataProcessor

    def getClassDefinition(self, moduleName: str, classId: int) -> "GameDataClassDefinition":
        return self._modules[moduleName]._classes[classId]

    def getCount(self, moduleName: str) -> int:
        if moduleName not in self._modules:
            self.initFromModuleName(moduleName)
        return self._modules[moduleName]._counter

    def getObject(self, moduleName: str, objectId) -> Any:
        return self._modules[moduleName].getObject(objectId)

    def getObjects(self, moduleName: str) -> list[object]:
        if moduleName not in self._modules:
            self.initFromModuleName(moduleName)
        return self._modules[moduleName].getObjects()

    def close(self) -> None:
        for module in self._modules:
            self._modules[module].close()
        self._modules = dict[str, ModuleReader]()
