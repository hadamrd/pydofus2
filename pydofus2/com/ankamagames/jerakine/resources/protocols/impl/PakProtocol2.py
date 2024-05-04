import json
import os
import traceback
from collections import defaultdict
from io import BufferedReader
from pathlib import Path
from typing import Dict

from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.resources.adapters.IAdapter import AdapterLoadError, IAdapter
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import IResourceObserver
from pydofus2.com.ankamagames.jerakine.resources.protocols.AbstractProtocol import AbstractProtocol
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class PakProtocol2(AbstractProtocol):

    _indexes = defaultdict(dict)

    def __init__(self):
        self._dataCount = None
        super().__init__()

    def getElementIndex(self, uri: Uri) -> Dict:
        if not self._indexes:
            fileStream = self.initStreamsIndexTable(uri)
            if not fileStream:
                raise Exception(f"Unable to init stream data for d2O protocol!")
        pathIndex = self._indexes.get(uri.path)
        if not pathIndex:
            Logger().warning(f"Unable to find stream index of the uri path : {uri.path}")
            return None
        subPathIndex = pathIndex.get(uri.subPath)
        if not subPathIndex:
            # Logger().warning(f"Unable to find stream index of the uri sub-path : {uri.subPath}. Available subPaths data {[k for k in pathIndex]}")
            return None
        return subPathIndex

    @property
    def indexes(self):
        return self._indexes

    def loadDirectly(self, uri: Uri) -> bytes:
        index = self.getElementIndex(uri)
        if not index:
            return
        with open(index["filePath"], "rb") as fp:
            fileStream = BinaryStream(fp, True)
            fileStream.seek(index["offset"])
            return fileStream.readBytes(index["length"])

    def load(
        self,
        uri: Uri,
        observer: "IResourceObserver",
        dispatchProgress: bool,
        cache: "ICache",
        forcedAdapter: "IAdapter",
        uniqueFile: bool,
    ) -> None:
        index = None
        data = bytearray()
        index = self.getElementIndex(uri)
        if not index:
            if observer:
                observer.onFailed(uri, "Unable to find the file in the container.", "FILE_NOT_FOUND_IN_PAK")
            return
        fileStream: BinaryStream = index["stream"]
        fileStream.seek(index["offset"])
        data = fileStream.readBytes(index["length"])
        self.getAdapter(uri, forcedAdapter)
        try:
            self._adapter.loadFromData(uri, data, observer, dispatchProgress)
        except AdapterLoadError as e:
            error_message = str(e)
            stack_trace = traceback.format_exc()
            formatted_message = (
                f"Error loading byte array from adapter (URI: {uri}):\n{error_message}\nStack Trace:\n{stack_trace}"
            )
            if observer:
                observer.onFailed(uri, formatted_message, "UNEXPECTED_ERROR")
            return

    def initStreamsIndexTable(self, uri: Uri) -> "BufferedReader":
        file_path = Path(uri.toFile())
        if not file_path.exists():
            raise FileNotFoundError(file_path)
        self._indexes[uri.path] = defaultdict(dict)
        while file_path and file_path.exists():
            fs = BinaryStream(file_path.open("rb"), True)
            vMax = fs.readUnsignedByte()
            vMin = fs.readUnsignedByte()
            if vMax != 2 or vMin != 1:
                return None
            fs.seek(-24, os.SEEK_END)
            dataOffset = fs.readUnsignedInt()
            dataCount = fs.readUnsignedInt()  # type: ignore
            indexOffset = fs.readUnsignedInt()
            indexCount = fs.readUnsignedInt()
            propertiesOffset = fs.readUnsignedInt()
            sub_files_indexes = self.getSubFilesIndexes(file_path, fs, indexOffset, indexCount, dataOffset)
            self._indexes[uri.path].update(sub_files_indexes)
            file_path = self.getNextFile(uri, fs, propertiesOffset)
        file_name_part = uri.path.replace("\\", "_")
        with open(f"gfx_{file_name_part}.json", "w") as fs:
            json.dump(self._indexes[uri.path], fs, indent=4)

    def getSubFilesIndexes(self, file_path, fs: BinaryStream, indexOffset, indexCount, dataOffset):
        indexes = {}
        fs.seek(indexOffset)
        for _ in range(indexCount):
            fileSubPath = str(fs.readUTF())
            fileOffset = fs.readUnsignedInt()
            fileLength = fs.readUnsignedInt()
            indexes[fileSubPath] = {
                "offset": fileOffset + dataOffset,
                "length": fileLength,
                "filePath": str(file_path),
            }
        return indexes

    def getNextFile(self, uri: Uri, fs: BinaryStream, propertiesOffset):
        fs.seek(propertiesOffset)
        propertyName = fs.readUTF()
        propertyValue = fs.readUTF()
        if propertyName == "link":
            idx = uri.path.rfind("\\")
            if idx != -1:
                uri = Uri(uri.path[:idx] + "/" + propertyValue)
            else:
                uri = Uri(propertyValue)
            return uri.toFile()
        return None

    def release(self):
        ...
