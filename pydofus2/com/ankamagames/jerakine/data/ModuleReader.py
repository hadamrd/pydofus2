import threading
from collections import OrderedDict
from functools import lru_cache
from typing import Any

from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.data.GameDataClassDefinition import GameDataClassDefinition
from pydofus2.com.ankamagames.jerakine.data.GameDataProcess import GameDataProcess
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.hurlan.crypto.Signature import Signature

lock = threading.Lock()


class InvalidD2OFile(Exception):
    pass


class ModuleReader:
    _clearObjectsCache = False

    def __init__(self, filepath: str, name: str) -> None:
        self.filepath = filepath
        self.name = name
        self.initModuleReader()

    def initModuleReader(self):
        with open(self.filepath, "rb") as f:
            stream = BinaryStream(f, True)
            self._streamStartIndex = 7
            self._classes = dict[str, GameDataClassDefinition]()
            self._counter = 0
            stream.seek(0)
            string_header = stream.readBytes(3)
            contentOffset = 0
            if string_header != b"D2O":
                if string_header != Signature.ANKAMA_SIGNED_FILE_HEADER:
                    raise InvalidD2OFile("Malformated game data file.")
                stream.readShort()
                contentOffset = stream.readInt()
                stream.seek(contentOffset, 1)
                self._streamStartIndex = stream.position + 7
                string_header = stream.readBytes(3)
                if string_header != b"D2O":
                    raise InvalidD2OFile("Malformated game data file.")
            indexesPointer = stream.readInt()
            stream.position = contentOffset + indexesPointer
            indexesLength = stream.readInt()
            self._indexes = OrderedDict()
            for _ in range(indexesLength // 8):
                key = stream.readInt()
                pointer = stream.readInt()
                self._indexes[key] = contentOffset + pointer
                self._counter += 1
            classesCount = stream.readInt()
            for _ in range(classesCount):
                classId = stream.readInt()
                self.__readClassDefinition(classId, stream)
            if stream.remaining():
                self._gameDataProcessor = GameDataProcess(stream, self.filepath)

    def clearObjectsCache(self):
        Logger().info(f"[Modulee {self.name}] Clearing objects cache.")
        self.getObjects.cache_clear()

    @lru_cache(maxsize=32, typed=False)
    def getObjects(self):
        with lock:
            if not self._counter:
                return None
            with open(self.filepath, "rb") as f:
                stream = BinaryStream(f, True)
                stream.seek(self._streamStartIndex)
                objects = list()
                for _ in range(self._counter):
                    classId = stream.readInt()
                    instance = self._classes[classId].from_stream(stream)
                    objects.append(instance)
            if ModuleReader._clearObjectsCache:
                BenchmarkTimer(60, self.clearObjectsCache).start()
            return objects

    def __readClassDefinition(self, classId, stream: BinaryStream):
        className = stream.readUTF()
        packageName = stream.readUTF()
        classDef = GameDataClassDefinition(packageName, className, self)
        fieldsCount = stream.readInt()
        for _ in range(fieldsCount):
            field = stream.readUTF()
            classDef.addField(field, stream)
        self._classes[classId] = classDef

    def getClassDefinition(self, object_id: int) -> GameDataClassDefinition:
        return self._classes[object_id]

    @lru_cache(maxsize=256, typed=False)
    def getObject(self, objectId: int) -> Any:
        with lock:
            if not self._indexes:
                Logger().warning(f"[Module {self.name}] No indexes found in the D2O file")
                return None
            pointer = self._indexes.get(objectId)
            if pointer is None:
                return None
            with open(self.filepath, "rb") as f:
                stream = BinaryStream(f, True)
                stream.seek(pointer)
                classId: int = stream.readInt()
                return self._classes[classId].from_stream(stream)

    def close(self) -> None:
        for stream in self._streams:
            try:
                if isinstance(stream, BinaryStream):
                    stream.close()
            except Exception as e:
                continue
        self._streams = None
        self._indexes = None
        self._classes = None
