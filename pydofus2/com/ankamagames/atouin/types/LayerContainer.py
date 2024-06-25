from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsItem

from pydofus2.com.ankamagames.atouin.types.CellContainer import CellContainer


class LayerContainer(QGraphicsItem):
    def __init__(self, nId):
        super().__init__()
        self._nLayerId = nId
        self.cells = list[CellContainer]()

    @property
    def layerId(self):
        return self._nLayerId

    def addCell(self, cellCtr: CellContainer):
        for i, cell in enumerate(self.cells):
            if cellCtr.depth < cell.depth:
                self.cells.insert(i, cellCtr)
                break
        else:
            self.cells.append(cellCtr)
        cellCtr.setParentItem(self)

    def boundingRect(self):
        rect = QRectF()
        for child in self.childItems():
            rect = rect.united(child.boundingRect().translated(child.pos()))
        return rect

    def paint(self, painter, option, widget=None):
        pass
