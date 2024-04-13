from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.data.map.elements.BasicElement import BasicElement
from pydofus2.com.ankamagames.atouin.enums.ElementTypesEnum import ElementTypesEnum
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray


class SoundElement(BasicElement):
    def __init__(self, cell: Cell):
        super().__init__(cell)
        self.mapVersion = None
        self.elementName = "Sound"
        self.soundId = None
        self.baseVolume = None
        self.fullVolumeDistance = None
        self.nullVolumeDistance = None
        self.minDelayBetweenLoops = None
        self.maxDelayBetweenLoops = None

    @property
    def elementType(self) -> ElementTypesEnum:
        return ElementTypesEnum.SOUND

    def fromRaw(self, raw: ByteArray, mapVersion: int) -> None:
        self.soundId = raw.readInt()
        self.baseVolume = raw.readShort()
        self.fullVolumeDistance = raw.readInt()
        self.nullVolumeDistance = raw.readInt()
        self.minDelayBetweenLoops = raw.readShort()
        self.maxDelayBetweenLoops = raw.readShort()
