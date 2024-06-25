from PyQt5.QtCore import QPoint, QRect, QRectF
from PyQt5.QtWidgets import QGraphicsItem


class BitmapCellContainer(QGraphicsItem):
    _destPoint: QPoint
    _srcRect: QRect
    _cellId: int = 0
    _layerId: int = 0
    _depth: int = 0
    datas: list
    bitmaps: list
    colorTransforms: list
    _numChildren: int = 0

    def __init__(self, cellId: int, parent=None):
        self.datas = []
        self.colorTransforms = []
        self._startX = 0
        self._startY = 0
        self._cellId = cellId
        super().__init__(parent)

    def boundingRect(self):
        rect = QRectF()
        for child in self.childItems():
            rect = rect.united(child.boundingRect().translated(child.pos()))
        return rect

    @property
    def cellId(self):
        return self._cellId

    @cellId.setter
    def cellId(self, value):
        self._cellId = value

    @property
    def layerId(self):
        return self._layerId

    @layerId.setter
    def layerId(self, value):
        self._layerId = value

    def addFakeChild(self, child: QGraphicsItem, data=None, colors=None):
        if colors:
            self.colorTransforms.append(colors)
        if data:
            self.datas.append(data)
        child.setParentItem(self)

    @property
    def startX(self) -> int:
        return self._startX

    @startX.setter
    def startX(self, val: int):
        self._startX = val

    @property
    def startY(self) -> int:
        return self._startY

    @startY.setter
    def startY(self, val: int):
        self._startY = val
