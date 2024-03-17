#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Exceptions


from collections import OrderedDict
from pathlib import Path

from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class InvalidD2PFile(Exception):
    def __init__(self, message):
        super(InvalidD2PFile, self).__init__(message)
        self.message = message


# Class itself
class Index:
    offset: int
    legth: int
    stream: BinaryStream

    def __init__(self, offset, length, stream) -> None:
        self.offset = offset
        self.length = length
        self.stream = stream

    def getStream(self) -> bytes:
        self.stream.seek(self.offset, 0)
        return self.stream.readBytes(self.length)


class PakProtocol2:
    """Read D2P files"""

    def __init__(self, filePath: Path):
        """Init the class with the informations about files in the pak2"""
        # Attributes
        self.dataOffset = None
        self.dataCount = None
        self.indexOffset = None
        self.indexCount = None
        self.propertiesOffset = None
        self.propertiesCount = None
        self.properties = None
        self.indexes = None
        self.streams = None
        self._loaded = False
        # Load the PAK file
        fs = BinaryStream(filePath.open("rb"), True)
        vMax = fs.readUnsignedByte()
        vMin = fs.readUnsignedByte()
        if vMax != 2 or vMin != 1:
            raise InvalidD2PFile("Invalid Pak2 file header.")
        fs.seek(-24, 2)  # Set position to end - 24 bytes

        self.dataOffset = fs.readUnsignedInt()
        self.dataCount = fs.readUnsignedInt()
        self.indexOffset = fs.readUnsignedInt()
        self.indexCount = fs.readUnsignedInt()
        self.propertiesOffset = fs.readUnsignedInt()
        self.propertiesCount = fs.readUnsignedInt()
        Logger().debug(f"dataOffset: {self.dataOffset}, dataCount : {self.dataCount}")
        Logger().debug(f"indexOffset: {self.indexOffset}, indexCount : {self.indexCount}")
        Logger().debug(f"propertiesOffset: {self.propertiesOffset}, propertiesCount : {self.propertiesCount}")

        if (
            self.dataOffset == b""
            or self.dataCount == b""
            or self.indexOffset == b""
            or self.indexCount == b""
            or self.propertiesOffset == b""
            or self.propertiesCount == b""
        ):
            raise InvalidD2PFile("The file doesn't match the D2P pattern.")

        # Read properties
        fs.seek(self.propertiesOffset, 0)
        self.properties = OrderedDict()

        for _ in range(self.propertiesCount):
            try:
                propertyName = fs.readUTF()
                propertyValue = fs.readUTF()
                self.properties[propertyName] = propertyValue
            except Exception as e:
                raise InvalidD2PFile("Error while reading properties!")

        # Read indexes
        fs.seek(self.indexOffset, 0)
        self.indexes = OrderedDict[str, Index]()
        for _ in range(self.indexCount):
            filePath = fs.readUTF()
            fileOffset = fs.readInt()
            fileLength = fs.readInt()
            if filePath == b"" or fileOffset == b"" or fileLength == b"":
                raise InvalidD2PFile("The file appears to be corrupt.")
            self.indexes[filePath] = Index(fileOffset + self.dataOffset, fileLength, fs)

    def iterStreams(self):
        for filePath, index in self.indexes.items():
            yield filePath, index.getStream()

    # Accessors

    def _get_properties(self):
        return self.properties

    @property
    def files(self):
        to_return = OrderedDict()
        for file_name, position in self.indexes.items():
            object_ = {"position": position}
            if self.streams:
                object_["binary"] = self.streams[file_name]
            to_return[file_name] = object_

        return to_return

    def _get_loaded(self):
        return self._loaded


class D2PBuilder:
    """Build D2P files"""

    def __init__(self, template, target):
        self._template = template
        self._stream = target
        self._base_offset = None
        self._base_length = None
        self._indexes_offset = None
        self._number_indexes = None
        self._properties_offset = None
        self._number_properties = None
        self._files_position = None
        self._files = None
        self._set_files(self._template.files)  # To update files and position

    def _set_files(self, files):
        self._files = files
        self._files_position = OrderedDict()

        # Update positions
        actual_offset = 0

        for file_name, specs in self._files.items():
            self._files_position[file_name] = {
                "offset": actual_offset,
                "length": len(specs["binary"]),
            }
            actual_offset += self._files_position[file_name]["length"]
