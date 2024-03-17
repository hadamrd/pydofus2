from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.flash.geom.Point import Point

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.atouin.data.map.Map import Map

import math


class Cell:
    def __init__(self, raw: BinaryStream, map: "Map", id: int):
        self.id = id
        self.map = map
        p = self.getCoords(self.id)
        self.x, self.y = p.x, p.y
        self.top_arrow = None
        self.bottom_arrow = None
        self.left_arrow = None
        self.right_arrow = None
        self.linkedZone = 1
        self.read(raw)

    @staticmethod
    def getId(x: int, y: int) -> int:
        return x + y * AtouinConstants.MAP_WIDTH

    @staticmethod
    def getCoords(cell_id):
        x = cell_id % AtouinConstants.MAP_WIDTH
        y = cell_id // AtouinConstants.MAP_WIDTH
        return Point(x, y)

    def read(self, raw: BinaryStream):
        self.floor = raw.readByte() * 10
        if self.floor == -1280:
            return

        if self.map.version >= 9:
            tmpbytesv9 = raw.readShort()
            self.mov = (tmpbytesv9 & 1) == 0
            self.nonWalkableDuringFight = (tmpbytesv9 & 2) != 0
            self.nonWalkableDuringRP = (tmpbytesv9 & 4) != 0
            self.los = (tmpbytesv9 & 8) == 0
            self.blue = (tmpbytesv9 & 16) != 0
            self.red = (tmpbytesv9 & 32) != 0
            self.visible = (tmpbytesv9 & 64) != 0
            self.farmCell = (tmpbytesv9 & 128) != 0

            if self.map.version == 9:
                self.top_arrow = (tmpbytesv9 & 256) != 0
                self.bottom_arrow = (tmpbytesv9 & 512) != 0
                self.right_arrow = (tmpbytesv9 & 1024) != 0
                self.left_arrow = (tmpbytesv9 & 2048) != 0

            else:
                self.havenbagCell = (tmpbytesv9 & 256) != 0
                self.top_arrow = (tmpbytesv9 & 512) != 0
                self.bottom_arrow = (tmpbytesv9 & 1024) != 0
                self.right_arrow = (tmpbytesv9 & 2048) != 0
                self.left_arrow = (tmpbytesv9 & 4096) != 0

        else:
            self.losmov = raw.readUnsignedByte()
            self.los = (self.losmov & 2) >> 1 == 1
            self.mov = (self.losmov & 1) == 1
            self.visible = (self.losmov & 64) >> 6 == 1
            self.farmCell = (self.losmov & 32) >> 5 == 1
            self.blue = (self.losmov & 16) >> 4 == 1
            self.red = (self.losmov & 8) >> 3 == 1
            self.nonWalkableDuringRP = (self.losmov & 128) >> 7 == 1
            self.nonWalkableDuringFight = (self.losmov & 4) >> 2 == 1

        self.speed = raw.readByte()
        self.mapChangeData = raw.readByte()

        if self.map.version > 5:
            self.moveZone = raw.readUnsignedByte()

        if self.map.version > 10 and (self.hasLinkedZoneRP() or self.hasLinkedZoneFight()):
            self.linkedZone = raw.readUnsignedByte()

        if 7 < self.map.version < 9:
            self.tmpBits = raw.readByte()
            self.arrow = 15 & self.tmpBits
            self.top_arrow = self.useTopArrow()
            self.bottom_arrow = self.useBottomArrow()
            self.left_arrow = self.useLeftArrow()
            self.right_arrow = self.useRightArrow()

    def useTopArrow(self) -> bool:
        if (self.arrow & 1) == 0:
            return False
        else:
            return True

    def useBottomArrow(self) -> bool:
        if (self.arrow & 2) == 0:
            return False
        else:
            return True

    def useRightArrow(self) -> bool:
        if (self.arrow & 4) == 0:
            return False
        else:
            return True

    def useLeftArrow(self) -> bool:
        if (self.arrow & 8) == 0:
            return False
        else:
            return True

    def hasLinkedZoneRP(self) -> bool:
        return self.mov and not self.farmCell

    def hasLinkedZoneFight(self) -> bool:
        return self.mov and not self.nonWalkableDuringFight and not self.farmCell and not self.havenbagCell

    def linkedZoneFight(self) -> int:
        return self.linkedZone & 15

    def isAccessibleDuringRP(self):
        return self.mov and not self.nonWalkableDuringRP

    def isAccessibleDuringFight(self):
        return self.mov and not self.nonWalkableDuringFight

    def allowsMapChange(self) -> bool:
        return self.mapChangeData != 0

    
    @property
    def linkedZoneRP(self):
        return (self.linkedZone & 240) >> 4

    @staticmethod
    def distanceBetween(cell1: "Cell", cell2: "Cell") -> float:
        return math.sqrt((cell1.x - cell2.x) ** 2 + (cell1.y - cell2.y) ** 2)

    @classmethod
    def cellPixelCoords(cls, cellId: int) -> Point:
        p: Point = cls.getCoords(cellId)
        p.x = p.x * AtouinConstants.CELL_WIDTH + (AtouinConstants.CELL_HALF_WIDTH if p.y % 2 == 1 else 0)
        p.y *= AtouinConstants.CELL_HALF_HEIGHT
        return p

    def __eq__(self, cell: "Cell"):
        return self.id == cell.id

    def __hash__(self) -> str:
        return self.id

    def __str__(self) -> str:
        return (
            "map : "
            + str(self.map.id)
            + ", CellId : "
            + str(self.id)
            + ", mov : "
            + str(self.mov)
            + ", los : "
            + str(self.los)
            + ", nonWalkableDuringFight : "
            + str(self.nonWalkableDuringFight)
            + ", nonWalkableDuringRp : "
            + str(self.nonWalkableDuringRP)
            + ", farmCell : "
            + str(self.farmCell)
            + ", havenbagCell: "
            + str(self.havenbagCell)
            + ", visbile : "
            + str(self.visible)
            + ", speed: "
            + str(self.speed)
            + ", moveZone: "
            + str(self.moveZone)
            + ", linkedZoneId: "
            + str(self.linkedZoneRP)
            + ", floor: "
            + str(self.floor)
        )
