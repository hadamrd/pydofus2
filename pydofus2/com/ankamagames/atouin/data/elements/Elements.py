from pydofus2.com.ankamagames.atouin.data.elements.GraphicalElementData import GraphicalElementData
from pydofus2.com.ankamagames.atouin.data.elements.GraphicalElementFactory import GraphicalElementFactory
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class DataFormatError(Exception):
    pass


class Elements(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.fileVersion = 0
        self.elementsCount = 0
        self._parsed = False
        self._failed = False
        self._elementsMap = {}
        self._jpgMap = {}
        self._elementsIndex = {}
        self._rawData = None

    @property
    def parsed(self):
        return self._parsed

    @property
    def failed(self):
        return self._failed

    def getElementData(self, elementId):
        return self._elementsMap.get(elementId, self.readElement(elementId))

    def isJpg(self, gfxId):
        return self._jpgMap.get(gfxId, False)

    def fromRaw(self, raw: BinaryStream):
        try:
            header = int(raw.readByte())
            if header != 69:
                raise DataFormatError("Unknown file format")
            self._rawData = raw
            self.fileVersion = raw.readByte()
            Logger().debug(f"File version : {self.fileVersion}")
            self.elementsCount = raw.readUnsignedInt()
            Logger().debug(f"Elements count : {self.elementsCount}")
            self._elementsMap = dict()
            self._elementsIndex = dict()
            skypLen = 0
            for _ in range(self.elementsCount):
                if self.fileVersion >= 9:
                    skypLen = raw.readUnsignedShort()
                edId = int(raw.readInt())
                if self.fileVersion <= 8:
                    self._elementsIndex[edId] = raw.position
                    self.readElement(edId)
                else:
                    self._elementsIndex[edId] = raw.position
                    raw.position = raw.position + skypLen - 4
            if self.fileVersion >= 8:
                gfxCount = raw.readInt()
                self._jpgMap = dict()
                for _ in range(gfxCount):
                    gfxId = raw.readInt()
                    self._jpgMap[gfxId] = True
            self._parsed = True
        except Exception as e:
            self._failed = True
            raise e

    def readElement(self, edId) -> GraphicalElementData:
        if edId not in self._elementsIndex:
            raise Exception(f"Element not found in elementsIndex")
        self._rawData.position = self._elementsIndex[edId]
        edType = self._rawData.readByte()
        ed = GraphicalElementFactory.getGraphicalElementData(edId, edType)
        if not ed:
            return None
        ed.fromRaw(self._rawData, self.fileVersion)
        self._elementsMap[edId] = ed
        return ed
