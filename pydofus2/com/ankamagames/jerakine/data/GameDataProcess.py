import functools
from ast import FunctionType
from collections.abc import Iterable

from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.data.I18nFileAccessor import I18nFileAccessor
from pydofus2.com.ankamagames.jerakine.enum.GameDataTypeEnum import GameDataTypeEnum


class GameDataProcess:
    def __init__(self, stream: BinaryStream, file_path: str):
        self._sortIndex = dict()
        self._queryableField = list()
        self._searchFieldIndex = dict()
        self._searchFieldCount = dict()
        self._searchFieldType = dict()
        self.filePath = file_path
        fieldListSize = stream.readInt()
        indexSearchOffset = stream.position + fieldListSize + 4
        while fieldListSize:
            size = stream.remaining()
            fieldName = stream.readUTF()
            self._queryableField.append(fieldName)
            self._searchFieldIndex[fieldName] = stream.readInt() + indexSearchOffset
            self._searchFieldType[fieldName] = stream.readInt()
            self._searchFieldCount[fieldName] = stream.readInt()
            fieldListSize = fieldListSize - (size - stream.remaining())

    def getQueryableField(self) -> dict[str, int]:
        return self._queryableField

    def getFieldType(self, fieldName: str) -> int:
        return self._searchFieldType.get(fieldName)

    @functools.lru_cache(maxsize=128)
    def query(self, fieldName: str, match: FunctionType) -> list[int]:
        with open(self.filePath, "rb") as f:
            stream = BinaryStream(f, True)
            result = list[int]()
            if not self._searchFieldIndex[fieldName]:
                return None
            type = self._searchFieldType[fieldName]
            readFct = self.getReadFunctionType(stream, type)
            itemCount = self._searchFieldCount[fieldName]
            stream.position = self._searchFieldIndex[fieldName]
            if readFct is None:
                return None
            for i in range(itemCount):
                if match(readFct()):
                    idsCount = stream.readInt() * 0.25
                    result = [stream.readInt() for _ in range(idsCount)]
                else:
                    stream.position(stream.readInt() + stream.position())
        return result

    @functools.lru_cache(maxsize=128)
    def queryEquals(self, fieldName: str, value) -> list[int]:
        with open(self.filePath, "rb") as f:
            stream = BinaryStream(f, True)
            result = list[int]()
            if not self._searchFieldIndex.get(fieldName):
                return None
            iterable = isinstance(value, Iterable)
            if iterable and len(value) == 0:
                return result
            if not iterable:
                value = [value]
            itemCount: int = self._searchFieldCount[fieldName]
            stream.seek(self._searchFieldIndex[fieldName])
            ftype: int = self._searchFieldType[fieldName]
            readFct: FunctionType = self.getReadFunctionType(stream, ftype)
            if readFct is None:
                return None
            valueIndex: int = 0
            value.sort()
            currentValue = value[0]
            for _ in range(itemCount):
                readValue = readFct()
                while readValue > currentValue:
                    valueIndex += 1
                    if valueIndex == len(value):
                        return result
                    currentValue = value[valueIndex]
                if readValue == currentValue:
                    idsCount = int(stream.readInt() * 0.25)
                    result = [stream.readInt() for _ in range(idsCount)]
                    valueIndex += 1
                    if valueIndex == len(value):
                        return result
                    currentValue = value[valueIndex]
                else:
                    stream.seek(stream.position + stream.readInt())
        return result

    def sort(self, fieldNames, ids: list[int], ascending=True) -> list[int]:
        ids.sort(key=functools.cmp_to_key(self.getSortFunction(fieldNames, ascending)))
        return ids

    def getSortFunction(self, fieldNames, ascending) -> FunctionType:
        if isinstance(fieldNames, str):
            fieldNames = [fieldNames]
        if isinstance(ascending, bool):
            ascending = [ascending]
        sortWay = list[float]()
        indexes = list[dict]()
        for i in fieldNames:
            fieldName = fieldNames[i]
            if GameDataTypeEnum(self._searchFieldType[fieldName]) == GameDataTypeEnum.I18N:
                self.buildI18nSortIndex(fieldName)
            else:
                self.buildSortIndex(fieldName)
            if len(ascending) < len(fieldNames):
                ascending.append(True)
            sortWay.append(1 if not ascending[i] else -1)
            indexes.append(self._sortIndex[fieldName])
        maxFieldIndex = len(fieldNames)

        def sortKey(t1: int, t2: int) -> float:
            for fieldIndex in range(maxFieldIndex):
                if indexes[fieldIndex][t1] < indexes[fieldIndex][t2]:
                    return -sortWay[fieldIndex]
                if indexes[fieldIndex][t1] > indexes[fieldIndex][t2]:
                    return sortWay[fieldIndex]
            return 0

        return sortKey

    def buildSortIndex(self, fieldName: str) -> None:
        with open(self.filePath, "rb") as f:
            stream = BinaryStream(f, True)
            if self._sortIndex[fieldName] or not self._searchFieldIndex[fieldName]:
                return
            itemCount: int = self._searchFieldCount[fieldName]
            stream.position = self._searchFieldIndex[fieldName]
            ref: dict = dict()
            self._sortIndex[fieldName] = ref
            type: int = self._searchFieldType[fieldName]
            readFct: FunctionType = self.getReadFunctionType(stream, type)
            if readFct == None:
                return
            for _ in range(itemCount):
                v = readFct()
                idsCount = stream.readInt() * 0.25
                for _ in range(idsCount):
                    ref[stream.readInt()] = v

    def buildI18nSortIndex(self, fieldName: str) -> None:
        with open(self.filePath, "rb") as f:
            stream = BinaryStream(f, True)
            if self._sortIndex[fieldName] or not self._searchFieldIndex[fieldName]:
                return
            itemCount: int = self._searchFieldCount[fieldName]
            stream.position = self._searchFieldIndex[fieldName]
            ref: dict = dict()
            self._sortIndex[fieldName] = ref
            for _ in range(itemCount):
                key = stream.readInt()
                idsCount = int(stream.readInt() * 0.25)
                if idsCount:
                    i18nOrder = I18nFileAccessor().getOrderIndex(key)
                    for _ in range(idsCount):
                        ref[stream.readInt()] = i18nOrder

    def readI18n(self) -> str:
        return I18nFileAccessor().getUnDiacriticalText(self._currentStream.readInt())

    def getReadFunctionType(self, stream: BinaryStream, type: GameDataTypeEnum) -> FunctionType:
        if type == GameDataTypeEnum.INT:
            readFct = stream.readInt
        elif type == GameDataTypeEnum.BOOLEAN:
            readFct = stream.readbool
        elif type == GameDataTypeEnum.STRING:
            readFct = stream.readUTF
        elif type == GameDataTypeEnum.NUMBER:
            readFct = stream.readDouble
        elif type == GameDataTypeEnum.I18N:
            I18nFileAccessor().useDirectBuffer(True)
            readFct = self.readI18n
            if not isinstance(stream, BinaryStream):
                directBuffer = BinaryStream()
                directBuffer.position = 0
                stream = directBuffer
                self._currentStream = stream
        elif type == GameDataTypeEnum.UINT:
            readFct = stream.readUnsignedInt
        return readFct
