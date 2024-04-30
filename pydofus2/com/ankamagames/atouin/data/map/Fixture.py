from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream


class Fixture:
    def __init__(self, raw):
        self.read(raw)

    def read(self, raw: BinaryStream):
        self.fixtureId: int = raw.readInt()
        self.offsetX: int = raw.readShort()
        self.offsetY: int = raw.readShort()
        self.rotation: float = raw.readShort()
        self.xScale: float = raw.readShort()
        self.yScale: float = raw.readShort()
        self.redMultiplier: int = raw.readByte()
        self.greenMultiplier: int = raw.readByte()
        self.blueMultiplier: int = raw.readByte()
        self.hue = self.redMultiplier | self.greenMultiplier | self.blueMultiplier
        self.alpha = raw.readUchar()
