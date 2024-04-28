import os
import threading
import xml.etree.ElementTree as ET
from functools import lru_cache
from time import perf_counter

from pydofus2.com.ankamagames.dofus import settings
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.managers.LangManager import LangManager
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import StoreDataManager
from pydofus2.com.ankamagames.jerakine.metaclass.ThreadSharedSingleton import ThreadSharedSingleton


class I18nFileAccessor(metaclass=ThreadSharedSingleton):

    _initialized = threading.Event()
    _initializing = threading.Event()

    def __init__(self) -> None:
        self.directBuffer = None
        if I18nFileAccessor._initialized.is_set():
            Logger().info("I18n file already loaded.")
            return
        if I18nFileAccessor._initializing.is_set():
            Logger().info("I18n file is already loading.")
            if not I18nFileAccessor._initialized.wait(10):
                raise RuntimeError("Wait for holder to initialise timedout")
            return
        self.LANG_FILE_PATH = self.getLangFile()
        self.initI18n()

    @staticmethod
    def getLangFile() -> BinaryStream:
        from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig

        xml_file_path = XmlConfig().getEntry("config.data.path.i18n.list")
        lang_files_dir = XmlConfig().getEntry("config.data.path.i18n")
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        files_dict = {}
        for file_elem in root.findall(".//file"):
            file_name = file_elem.get("name")
            if file_name:
                full_path = os.path.join(lang_files_dir, file_name)
                if os.path.exists(full_path):
                    files_dict[file_name] = full_path
        lastLang = StoreDataManager().getData(settings.DATASTORE_LANG_VERSION, "lastLang")
        file_name = None
        if lastLang:
            file_name = f"i18n_{lastLang}.d2i"
        else:
            # Get any file but in preference current if exists
            file_name = XmlConfig().getEntry("config.lang.current")
            if not file_name in files_dict:
                file_name = list(files_dict.keys())[0]
        if file_name is None:
            raise RuntimeError("No lang file found")
        return files_dict[file_name]

    def initI18n(self):
        self._initializing.set()
        Logger().info("Loading I18n file...")
        s = perf_counter()
        with open(self.LANG_FILE_PATH, "rb") as fp:
            stream = BinaryStream(fp, big_endian=True)
            self.indexes = dict()
            self.unDiacriticalIndex = dict()
            self.textIndexes = dict()
            self.textIndexesOverride = dict()
            self.textSortIndex = dict()
            self.textCount = 0
            indexesPointer: int = stream.readInt()
            keyCount: int = 0
            stream.position = indexesPointer
            indexesLength: int = stream.readInt()
            i = 0
            while i < indexesLength:
                key = stream.readInt()
                diacriticalText = stream.readbool()
                pointer = stream.readInt()
                i += 9
                self.indexes[key] = pointer
                keyCount += 1
                if diacriticalText:
                    keyCount += 1
                    i += 4
                    self.unDiacriticalIndex[key] = stream.readInt()
                else:
                    self.unDiacriticalIndex[key] = pointer
            indexesLength = stream.readInt()
            while indexesLength > 0:
                position = stream.position
                textKey = stream.readUTF()
                pointer = stream.readInt()
                self.textCount += 1
                self.textIndexes[textKey] = pointer
                indexesLength -= stream.position - position
            indexesLength = stream.readInt()
            i = 0
            while indexesLength > 0:
                position = stream.position
                i += 1
                self.textSortIndex[stream.readInt()] = i
                indexesLength -= stream.position - position
            textKeys: list = []
            for textKey in self.textIndexes:
                textKeys.append(textKey)
        for textKey in textKeys:
            self.setEntries(textKey)
        self._initializing.clear()
        self._initialized.set()
        Logger().info(f"Loaded {keyCount} keys and {self.textCount} texts. in {perf_counter() - s}s")

    def logInit() -> None:
        Logger().debug("Initialized !")

    def setEntries(self, textKey: str) -> None:
        LangManager().setEntry(textKey, self.getNamedText(textKey))

    def overrideId(self, oldId: int, newId: int) -> None:
        self.indexes[oldId] = self.indexes[newId]
        self.unDiacriticalIndex[oldId] = self.unDiacriticalIndex[newId]

    def getOrderIndex(self, key: int) -> int:
        return self.textSortIndex[key]

    @lru_cache(maxsize=128)
    def getText(self, key: int) -> str:
        if not self.indexes:
            return None
        pointer = self.indexes.get(key)
        if not pointer:
            return None
        if self.directBuffer is None:
            with open(self.LANG_FILE_PATH, "rb") as fp:
                stream = BinaryStream(fp, big_endian=True)
                stream.position = pointer
                return stream.readUTF()
        self.directBuffer.position = pointer
        return self.directBuffer.readUTF()

    @lru_cache(maxsize=128)
    def getUnDiacriticalText(self, key: int) -> str:
        if not self.unDiacriticalIndex:
            return None
        pointer: int = self.unDiacriticalIndex.get(key)
        if not pointer:
            return None
        with open(self.LANG_FILE_PATH, "rb") as fp:
            stream = BinaryStream(fp, big_endian=True)
            if self.directBuffer is None:
                stream.position = pointer
                return stream.readUTF()
        self.directBuffer.position = pointer
        return self.directBuffer.readUTF()

    def hasText(self, key: int) -> bool:
        return self.indexes and key in self.indexes

    @lru_cache(maxsize=128)
    def getNamedText(self, textKey: str) -> str:
        if not self.textIndexes:
            return None
        if textKey in self.textIndexesOverride:
            textKey = self.textIndexesOverride[textKey]
        pointer = self.textIndexes.get(textKey)
        if not pointer:
            return None
        with open(self.LANG_FILE_PATH, "rb") as fp:
            stream = BinaryStream(fp, big_endian=True)
            stream.position = pointer
            return stream.readUTF()

    def hasNamedText(self, textKey: str) -> bool:
        return self.textIndexes and self.textIndexes[textKey]

    def useDirectBuffer(self, bool: bool) -> None:
        if self.directBuffer == bool:
            return
        if not bool:
            self.directBuffer = None
        else:
            self.directBuffer = BinaryStream()
            with open(self.LANG_FILE_PATH, "rb") as fp:
                stream = BinaryStream(fp, big_endian=True)
                stream.position = 0
                self.directBuffer.writeBytes(stream.readBytes())

    def close(self) -> None:
        self.indexes.clear()
        self.textIndexes.clear()
        self.directBuffer.close()
