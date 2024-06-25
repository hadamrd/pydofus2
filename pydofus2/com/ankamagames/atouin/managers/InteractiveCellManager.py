from pydofus2.com.ankamagames.atouin.Atouin import Atouin
from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.types.GraphicCell import GraphicCell
from pydofus2.com.ankamagames.atouin.utils.CellUtil import CellUtil
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton


class InteractiveCellManager(metaclass=Singleton):
    def __init__(self):
        self._aCells = dict[int, GraphicCell]()
        self._aCellPool = dict[int, GraphicCell]()
        self._bShowGrid = Atouin().options.getOption("alwaysShowGrid")
        self._showEveryCellId = Atouin().options.getOption("showEveryCellId")
        self.init()

    def init(self):
        for cellId in range(AtouinConstants.MAP_CELLS_COUNT):
            c = GraphicCell(cellId)
            c.mouseEnabled = False
            c.mouseChildren = False
            self._aCellPool[cellId] = c

    def getCell(self, cellId) -> GraphicCell:
        if cellId > CellUtil.MAX_CELL_ID or cellId < CellUtil.MIN_CELL_ID:
            return None
        self._aCells[cellId] = self._aCellPool[cellId]
        return self._aCells[cellId]
