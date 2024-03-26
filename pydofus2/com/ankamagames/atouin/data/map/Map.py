from typing import List, Tuple, cast

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import \
    NormalGraphicalElementData
from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.data.map.elements.GraphicalElement import \
    GraphicalElement
from pydofus2.com.ankamagames.atouin.data.map.Fixture import Fixture
from pydofus2.com.ankamagames.atouin.data.map.Layer import Layer
from pydofus2.com.ankamagames.atouin.enums.ElementTypesEnum import \
    ElementTypesEnum
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import \
    DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class Map:
    def __init__(self, raw: BinaryStream, id, version: int):
        self.id = id
        self.version = version
        self.topArrowCell = set[int]()
        self.bottomArrowCell = set[int]()
        self.leftArrowCell = set[int]()
        self.rightArrowCell = set[int]()
        self.cells = dict[int, Cell]()
        self.oldMvtSystem = False
        self.isUsingNewMovementSystem = False
        self._parser = False
        self._gfxList: list[NormalGraphicalElementData] = None
        self._gfxCell = dict[int, int]()
        self.fromRaw(raw)

    def fromRaw(self, raw: BinaryStream):
        self.relativeId = raw.readUnsignedInt()
        self.mapType = raw.readByte()
        self.subareaId = raw.readInt()
        self.topNeighbourId = raw.readInt()
        self.bottomNeighbourId = raw.readInt()
        self.leftNeighbourId = raw.readInt()
        self.rightNeighbourId = raw.readInt()
        self.shadowBonusOnEntities = raw.readUnsignedInt()

        if self.version >= 9:
            read_color = raw.readInt()
            self.backgroundAlpha = (read_color & 4278190080) >> 32
            self.backgroundRed = (read_color & 16711680) >> 16
            self.backgroundGreen = (read_color & 65280) >> 8
            self.backgroundBlue = read_color & 255
            read_color = raw.readUnsignedInt()
            grid_alpha = (read_color & 4278190080) >> 32
            grid_red = (read_color & 16711680) >> 16
            grid_green = (read_color & 65280) >> 8
            grid_blue = read_color & 255
            self.gridColor = (
                (grid_alpha & 255) << 32 | (grid_red & 255) << 16 | (grid_green & 255) << 8 | grid_blue & 255
            )

        elif self.version >= 3:
            self.backgroundRed = raw.readByte()
            self.backgroundGreen = raw.readByte()
            self.backgroundBlue = raw.readByte()

        self.backgroundColor = (
            (self.backgroundAlpha & 255) << 32
            | (self.backgroundRed & 255) << 16
            | (self.backgroundGreen & 255) << 8
            | self.backgroundBlue & 255
        )

        if self.version >= 4:
            self.zoomScale = raw.readUnsignedShort() // 100
            self.zoomOffsetX = raw.readShort()
            self.zoomOffsetY = raw.readShort()
            if self.zoomScale < 1:
                self.zoomScale = 1
                self.zoomOffsetX = self.zoomOffsetY = 0

        if self.version > 10:
            self.tacticalModeTemplateId = raw.readInt()

        self.backgroundsCount = raw.readByte()
        self.backgroundFixtures = [Fixture(raw) for _ in range(self.backgroundsCount)]

        self.foregroundsCount = raw.readByte()
        self.foregroundsFixtures = [Fixture(raw) for _ in range(self.foregroundsCount)]

        raw.readInt()
        self.groundCRC = raw.readInt()
        self.layersCount = raw.readByte()
        self.layers = [Layer(raw, self.version) for _ in range(self.layersCount)]

        for cellid in range(AtouinConstants.MAP_CELLS_COUNT):
            cell = Cell(raw, self, cellid)
            self.cells[cellid] = cell

            if not self.oldMvtSystem:
                self.oldMvtSystem = cell.moveZone
            if cell.moveZone != self.oldMvtSystem:
                self.isUsingNewMovementSystem = True

            if cell.top_arrow:
                self.topArrowCell.add(cellid)

            elif cell.bottom_arrow:
                self.bottomArrowCell.add(cellid)

            elif cell.left_arrow:
                self.leftArrowCell.add(cellid)

            elif cell.right_arrow:
                self.rightArrowCell.add(cellid)

        self._parser = True

    def getNeighbourCellFromDirection(cls, srcId: int, direction: DirectionsEnum) -> "Cell":
        if (srcId // AtouinConstants.MAP_WIDTH) % 2 == 0:
            offsetId = 0

        else:
            offsetId = 1

        if direction == DirectionsEnum.RIGHT:
            destId = srcId + 1
            if destId % AtouinConstants.MAP_WIDTH != 0:
                return cls.cells[destId]
            return None

        elif direction == DirectionsEnum.DOWN_RIGHT:
            destId = srcId + AtouinConstants.MAP_WIDTH + offsetId
            if destId < AtouinConstants.MAP_CELLS_COUNT and (srcId + 1) % (AtouinConstants.MAP_WIDTH * 2) != 0:
                return cls.cells[destId]
            return None

        elif direction == DirectionsEnum.DOWN:
            destId = srcId + AtouinConstants.MAP_WIDTH * 2
            if destId < AtouinConstants.MAP_CELLS_COUNT:
                return cls.cells[destId]
            return None

        elif direction == DirectionsEnum.DOWN_LEFT:
            destId = srcId + AtouinConstants.MAP_WIDTH - 1 + offsetId
            if destId < AtouinConstants.MAP_CELLS_COUNT and srcId % (AtouinConstants.MAP_WIDTH * 2) != 0:
                return cls.cells[destId]
            return None

        elif direction == DirectionsEnum.LEFT:
            destId = srcId - 1
            if srcId % AtouinConstants.MAP_WIDTH != 0:
                return cls.cells[destId]
            return None

        elif direction == DirectionsEnum.UP_LEFT:
            destId = srcId - AtouinConstants.MAP_WIDTH - 1 + offsetId
            if destId >= 0 and srcId % (AtouinConstants.MAP_WIDTH * 2) != 0:
                return cls.cells[destId]
            return None

        elif direction == DirectionsEnum.UP:
            destId = srcId - AtouinConstants.MAP_WIDTH * 2
            if destId >= 0:
                return cls.cells[destId]
            return None

        elif direction == DirectionsEnum.UP_RIGHT:
            destId = srcId - AtouinConstants.MAP_WIDTH + offsetId
            if destId > 0 and (srcId + 1) % (AtouinConstants.MAP_WIDTH * 2) != 0:
                return cls.cells[destId]
            return None

        raise Exception("Invalid direction.")

    def getCellNeighbours(self, cellId: int, allowThrought: bool = True) -> set["Cell"]:
        from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import \
            DataMapProvider

        currMp = MapPoint.fromCellId(cellId)
        neighbours = set[Cell]()
        for i in DirectionsEnum:
            cell = self.getNeighbourCellFromDirection(cellId, i)
            if cell and cell.isAccessibleDuringRP():
                canMovTo = DataMapProvider().pointMov(currMp._nX, currMp._nY, allowThrought, cell.id, dataMap=self)
                if canMovTo:
                    neighbours.add(cell)
        return neighbours

    def getDirectionToNeighbor(self, dstMapId):
        Logger().debug("current map id: %d", self.id)
        for direction in DirectionsEnum.getMapChangeDirections():
            neighbour = self.getNeighborIdFromDirection(direction)
            Logger().debug("Neighbour: %s", neighbour)
            if int(neighbour) == int(dstMapId):
                return direction

    def getNeighborIdFromDirection(self, direction: DirectionsEnum) -> int:
        if direction == DirectionsEnum.LEFT:
            return self.leftNeighbourId
        elif direction == DirectionsEnum.RIGHT:
            return self.rightNeighbourId
        elif direction == DirectionsEnum.UP:
            return self.topNeighbourId
        elif direction == DirectionsEnum.DOWN:
            return self.bottomNeighbourId
        else:
            raise Exception("invalid direction : " + str(direction))

    def printGrid(self):
        format_row = "{:>2}" * (AtouinConstants.MAP_WIDTH + 2)
        print(format_row.format(*[" "] * (AtouinConstants.MAP_WIDTH + 2)))
        for j in range(2 * AtouinConstants.MAP_HEIGHT):
            row = []
            for i in range(AtouinConstants.MAP_WIDTH):
                row.append(" " if self.cells[i + j * AtouinConstants.MAP_WIDTH].isAccessibleDuringRP() else "X")
            print(format_row.format(" ", *row, " "))
        print(format_row.format(*[" "] * (AtouinConstants.MAP_WIDTH + 2)))

    def getGfxList(self, skipBackground: bool = False) -> List[NormalGraphicalElementData]:
        if self._gfxList is None:
            self.computeGfxList(skipBackground)
        return self._gfxList

    def getGfxCount(self, gfxId: int) -> int:
        if self._gfxList is None:
            self.computeGfxList()
        return self._gfxCount.get(gfxId, 0)

    def getBorderCells(self, direction: DirectionsEnum):
        currentlyCheckedCellX = None
        currentlyCheckedCellY = None

        if direction == DirectionsEnum.RIGHT:
            currentlyCheckedCellX = AtouinConstants.MAP_WIDTH - 1
            currentlyCheckedCellY = AtouinConstants.MAP_WIDTH - 1

        elif direction == DirectionsEnum.LEFT:
            currentlyCheckedCellX = 0
            currentlyCheckedCellY = 0

        elif direction == DirectionsEnum.DOWN:
            currentlyCheckedCellX = AtouinConstants.MAP_HEIGHT - 1
            currentlyCheckedCellY = -(AtouinConstants.MAP_HEIGHT - 1)

        elif direction == DirectionsEnum.UP:
            currentlyCheckedCellX = 0
            currentlyCheckedCellY = 0

        res = []

        if direction == DirectionsEnum.RIGHT or direction == DirectionsEnum.LEFT:
            maxI = AtouinConstants.MAP_HEIGHT * 2
            for i in range(maxI):
                currentCellId = MapPoint.fromCoords(currentlyCheckedCellX, currentlyCheckedCellY).cellId
                cellData = self.cells[currentCellId]
                mapChangeData = cellData.mapChangeData
                if mapChangeData and (
                    direction == DirectionsEnum.RIGHT
                    and (
                        mapChangeData & 1
                        or (currentCellId + 1) % (AtouinConstants.MAP_WIDTH * 2) == 0
                        and mapChangeData & 2
                        or (currentCellId + 1) % (AtouinConstants.MAP_WIDTH * 2) == 0
                        and mapChangeData & 128
                    )
                    or direction == DirectionsEnum.LEFT
                    and (
                        currentlyCheckedCellX == -currentlyCheckedCellY
                        and mapChangeData & 8
                        or mapChangeData & 16
                        or currentlyCheckedCellX == -currentlyCheckedCellY
                        and mapChangeData & 32
                    )
                ):
                    res.append(currentCellId)
                if not (i % 2):
                    currentlyCheckedCellX += 1
                else:
                    currentlyCheckedCellY -= 1

        elif direction == DirectionsEnum.DOWN or direction == DirectionsEnum.UP:
            for i in range(AtouinConstants.MAP_WIDTH * 2):
                currentCellId = MapPoint.fromCoords(currentlyCheckedCellX, currentlyCheckedCellY).cellId
                cellData = self.cells[currentCellId]
                mapChangeData = cellData.mapChangeData
                if mapChangeData and (
                    direction == DirectionsEnum.UP
                    and (
                        currentCellId < AtouinConstants.MAP_WIDTH
                        and mapChangeData & 32
                        or mapChangeData & 64
                        or currentCellId < AtouinConstants.MAP_WIDTH
                        and mapChangeData & 128
                    )
                    or direction == DirectionsEnum.DOWN
                    and (
                        currentCellId >= AtouinConstants.MAP_CELLS_COUNT - AtouinConstants.MAP_WIDTH
                        and mapChangeData & 2
                        or mapChangeData & 4
                        or currentCellId >= AtouinConstants.MAP_CELLS_COUNT - AtouinConstants.MAP_WIDTH
                        and mapChangeData & 8
                    )
                ):
                    res.append(currentCellId)
                if not (i % 2):
                    currentlyCheckedCellX += 1
                else:
                    currentlyCheckedCellY += 1

        return res

    def getGfxCell(self, gfxId):
        return self._gfxCell.get(gfxId)

    def getIdentifiedElements(self) -> List[Tuple[MapPoint, GraphicalElement]]:
        identifiedElements = list[Tuple[MapPoint, GraphicalElement]]()
        for layer in self.layers:
            if layer.layerId == Layer.LAYER_GROUND:
                continue
            for cell in layer.cells:
                for element in cell.elements:
                    if element.elementType == ElementTypesEnum.GRAPHICAL:
                        element = cast(GraphicalElement, element)
                        if element.identifier > 0:
                            identifiedElements.append([MapPoint.fromCellId(cell.cellId), element])
        return identifiedElements

    def computeGfxList(self, skipBackground=False, layersFilter=[]) -> list[NormalGraphicalElementData]:
        gfxList = {}
        self._gfxCount = {}
        numLayer = len(self.layers)
        for l in range(numLayer):
            layer = self.layers[l]
            if layersFilter and layer.layerId not in layersFilter:
                continue
            layer.layerId
            if not (skipBackground and l == 0):
                lsCell = layer.cells
                numCell = len(lsCell)
                for c in range(numCell):
                    cell = lsCell[c]
                    lsElement = cell.elements
                    numElement = len(lsElement)
                    for e in range(numElement):
                        element = lsElement[e]
                        if element.elementType == ElementTypesEnum.GRAPHICAL:
                            element = cast(GraphicalElement, element)
                            elementId = element.elementId
                            elementData = Elements().getElementData(elementId)
                            if elementData is None:
                                Logger().error("Error: Unknown graphical element ID " + str(elementId))
                            elif isinstance(elementData, NormalGraphicalElementData):
                                graphicalElementData = elementData
                                self._gfxCell[graphicalElementData.gfxId] = cell.cellId
                                gfxList[graphicalElementData.gfxId] = graphicalElementData
                                if graphicalElementData.gfxId in self._gfxCount:
                                    self._gfxCount[graphicalElementData.gfxId] += 1
                                else:
                                    self._gfxCount[graphicalElementData.gfxId] = 1
        self._gfxList = list(gfxList.values())
        return self._gfxList
