#!/usr/bin/python3
# -*- coding: utf-8 -*-
import io
import tempfile
import zlib

from pydofus2.com.ankamagames.atouin.data.map.Map import Map
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class InvalidDLMFile(Exception):
    pass


class DLM:
    def __init__(self, key=None):
        if key == None:
            raise InvalidDLMFile("Map decryption key is empty.")
        self._key = key

    def setKey(self, key):
        self._key = key

    def read(self, raw: bytes):
        dlm_uncompressed = tempfile.TemporaryFile()
        dlm_uncompressed.write(zlib.decompress(raw))
        dlm_uncompressed.seek(0)
        dlm_raw = BinaryStream(dlm_uncompressed, True)

        header = dlm_raw.readByte()
        if header != 77:
            raise InvalidDLMFile("Unknown file format.")
        
        
        map_version = dlm_raw.readByte()
        id = dlm_raw.readUnsignedInt()

        if map_version >= 7:
            self.encrypted = dlm_raw.readbool()
            self.encryptionVersion = dlm_raw.readByte()
            self.dataLen = dlm_raw.readInt()
            if self.encrypted:
                Logger().debug(f"Map is encrypted with version {self.encryptionVersion}")
                if not self._key:
                    raise Exception("Map decryption key is empty.")
                self.encryptedData = dlm_raw.readBytes(self.dataLen)
                decryptedData = bytearray()
                for i in range(self.dataLen):
                    decryptedData.append(self.encryptedData[i] ^ ord(self._key[i % len(self._key)]))
                cleanData = io.BytesIO(decryptedData)
                raw = BinaryStream(cleanData, True)
            else:
                raw = dlm_raw
        map = Map(raw, id, map_version)
        dlm_uncompressed.close()
        del dlm_raw
        return map
