from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsPixmapItem


class BitmapCellContainer(QGraphicsItemGroup):
    def __init__(self, id: int, parent=None):
        super().__init__(parent)
        self._cellId = id
        self._layerId = 0
        self._startX = 0
        self._startY = 0
        self._x = 0.0
        self._y = 0.0
        self._depth = 0
        self.layers = list[QGraphicsPixmapItem]()
        self._mouseEnabled = True

    def addLayer(self, image_bytes):
        pixmap = QPixmap()
        if pixmap.loadFromData(image_bytes):
            item = QGraphicsPixmapItem(pixmap, self)
            self.layers.append(item)
            return item
        else:
            print("Failed to load image data")
            return None

    def setPosition(self, x, y):
        self.setPos(x, y)

    @property
    def cellId(self):
        return self._cellId

    @cellId.setter
    def cellId(self, value):
        self._cellId = value

    @property
    def mouseEnabled(self):
        return self._mouseEnabled

    @mouseEnabled.setter
    def mouseEnabled(self, value):
        self._mouseEnabled = value
        for layer in self.layers:
            layer.setAcceptHoverEvents(value)
            if value:
                layer.setAcceptedMouseButtons(Qt.LeftButton)  # Assuming you want left clicks
            else:
                layer.setAcceptedMouseButtons(Qt.NoButton)
