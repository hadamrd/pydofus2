import math

from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import \
    MapDisplayManager


class CellUtil:

    MAX_CELL_ID: int = 559

    MIN_CELL_ID: int = 0

    def __init__(self):
        super().__init__()

    def isLeftCol(self, cellId: int) -> bool:
        return cellId % 14 == 0

    def isRightCol(self, cellId: int) -> bool:
        return self.isLeftCol(cellId + 1)

    def isTopRow(self, cellId: int) -> bool:
        return cellId < 28

    def isBottomRow(self, cellId: int) -> bool:
        return cellId > 531

    def isEvenRow(self, cellId: int) -> bool:
        return math.floor(cellId / 14) % 2 == 0

    def isValidCellIndex(self, cellId: int) -> bool:
        return bool(cellId >= 0 and cellId < len(MapDisplayManager().dataMap.cells))
