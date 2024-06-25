from PyQt5.QtCore import QRect

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import (
    NormalGraphicalElementData,
)
from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.data.map.Map import Map
from pydofus2.com.ankamagames.atouin.enums.ElementTypesEnum import ElementTypesEnum
from pydofus2.com.ankamagames.atouin.Frustum import Frustum
from pydofus2.com.ankamagames.atouin.types.miscs.PartialDataMap import PartialDataMap
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.positions.WorldPoint import WorldPoint
from pydofus2.DofusUI.StageShareManager import StageShareManager


class VisibleCellDetection:
    @staticmethod
    def detectCell(visible, map: Map, pMap: WorldPoint, frustum: Frustum, currentMapPoint: MapPoint):
        if currentMapPoint is None:
            Logger().error("Current map point is required")
            return None

        pdm = PartialDataMap()
        ox = (pMap.x - currentMapPoint.x) * AtouinConstants.CELL_WIDTH * AtouinConstants.MAP_WIDTH
        oy = (pMap.y - currentMapPoint.y) * AtouinConstants.CELL_HEIGHT * AtouinConstants.MAP_HEIGHT
        rv = QRect(
            -frustum.x / frustum.scale,
            -frustum.y / frustum.scale,
            StageShareManager().startHeight / frustum.scale,
            StageShareManager().startHeight / frustum.scale,
        )

        rcv = QRect()
        aCell = {}
        aGfx = {}

        elements = Elements()
        for layer in map.layers:
            for cell in layer.cells:
                alt = 0
                width = 0
                left = 100000
                bottom = 0
                aGfx = []
                for element in cell.elements:
                    if element.elementType == ElementTypesEnum.GRAPHICAL:
                        elementData = elements.getElementData(element.elementId)
                        bottomTmp = element.altitude * AtouinConstants.ALTITUDE_PIXEL_UNIT
                        bottom = min(bottomTmp, bottom)
                        if isinstance(elementData, NormalGraphicalElementData):
                            ged = elementData
                            left = min(-ged.originX + AtouinConstants.CELL_WIDTH, left)
                            width = max(ged.sizeX, width)
                            alt += ged.originY + ged.sizeY
                            aGfx.append(ged.gfxId)
                        else:
                            alt += abs(bottomTmp)
                if not alt:
                    alt = AtouinConstants.CELL_HEIGHT
                if left == 100000:
                    left = 0
                if width < AtouinConstants.CELL_WIDTH:
                    width = AtouinConstants.CELL_WIDTH

                p = Cell.cellPixelCoords(cell.cellId)
                rcv = QRect(
                    p.x + ox + left - AtouinConstants.CELL_HALF_WIDTH,
                    p.y + oy - bottom - alt,
                    width,
                    alt + AtouinConstants.CELL_HEIGHT * 2,
                )
                if cell.cellId not in aCell:
                    aCell[cell.cellId] = {"r": rcv.copy(), "gfx": aGfx}
                else:
                    aCell[cell.cellId]["r"] = aCell[cell.cellId]["r"].union(rcv)
                    aCell[cell.cellId]["gfx"].extend(aGfx)

        for i in range(len(aCell)):
            if aCell[i]:
                rcv = aCell[i]["r"]
                if rcv and rcv.intersects(rv) == visible:
                    pdm.cell[i] = True
                    for j in aCell[i]["gfx"]:
                        aGfx[j] = True

        for s in aGfx:
            pdm.gfx.append(s)

        return pdm
