from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem


class SimpleGraphicsContainer(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self._opaqueBackground = None
        self._background = QGraphicsRectItem(self)
        self._background.setBrush(QColor("transparent"))
        self._background.setZValue(-1)
        self._background.setPen(QPen(Qt.NoPen))

    @property
    def opaqueBackground(self):
        return self._opaqueBackground

    @opaqueBackground.setter
    def opaqueBackground(self, rgb: int):
        self._opaqueBackground = rgb
        self._background.setBrush(QBrush(QColor(rgb)))

    def boundingRect(self):
        rect = QRectF()
        for child in self.childItems():
            if child == self._background:
                continue
            rect = rect.united(child.boundingRect().translated(child.pos()))
        self._background.setRect(rect)
        return rect

    def paint(self, painter, option, widget=None):
        pass

    def addChild(self, item: QGraphicsItem):
        item.setParentItem(self)

    def removeChild(self, item: QGraphicsItem):
        if item.parentItem() == self:
            item.setParentItem(None)
