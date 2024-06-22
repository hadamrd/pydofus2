from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem

from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.flash.geom.ColorTransform import ColorTransform


class CellContainer(QGraphicsItem):
    _ratio = None  # Presuming this should be a class variable as in ActionScript
    cltr: ColorTransform

    def __init__(self, id: int):
        super().__init__()  # Calling the constructor of the base class Sprite
        self._cellId = id
        self.name = "Cell_" + str(self._cellId)
        self._layerId = 0
        self._startX = 0
        self._startY = 0
        self._depth = 0

    @property
    def cellId(self) -> int:
        return self._cellId

    @cellId.setter
    def cellId(self, val: int):
        self._cellId = val

    @property
    def layerId(self) -> int:
        return self._layerId

    @layerId.setter
    def layerId(self, val: int):
        self._layerId = val

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

    @property
    def depth(self) -> int:
        return self._depth

    @depth.setter
    def depth(self, val: int):
        self._depth = val

    def addFakeChild(self, pChild: QGraphicsItem, pData=None, colors=None):
        if self._ratio is None:
            val = XmlConfig().getEntry("config.gfx.world.scaleRatio")
            self._ratio = 1 if val is None else float(val)

        if pData is not None:
            if isinstance(pChild, QGraphicsPixmapItem):
                pChild.setPos(pData.x * self._ratio, pData.y * self._ratio)
            else:
                pChild.setPos(pData.x, pData.y)
            pChild.alpha = pData.alpha
            pChild.scaleX = pData.scaleX
            pChild.scaleY = pData.scaleY

        if colors is not None:
            cltr = ColorTransform(colors["red"], colors["green"], colors["blue"], colors["alpha"])
            transformedImage = cltr.apply(pChild.pixmap().toImage())
            pChild.setPixmap(QPixmap.fromImage(transformedImage))

        pChild.setParentItem(self)

    def boundingRect(self):
        rect = QRectF()
        for child in self.childItems():
            rect = rect.united(child.boundingRect().translated(child.pos()))
        return rect

    def paint(self, painter, option, widget=None):
        pass
