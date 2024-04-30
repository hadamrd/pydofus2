from PyQt5.QtCore import QRectF, pyqtSignal
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsObject


class FrustumShape(QGraphicsObject):
    clicked = pyqtSignal(object)
    hoverEnter = pyqtSignal(object)
    hoverLeave = pyqtSignal(object)
    mouseMove = pyqtSignal(object)

    def __init__(self, direction, x=0, y=0, width=100, height=100, color=None):
        super().__init__()
        if not color:
            color = QColor(0, 0, 0, 0)
        self._direction = direction
        self._rect = QRectF(x, y, width, height)  # Storing geometry
        self._color = color  # Storing the color
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return self._rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self._color))
        painter.drawRect(self._rect)

    def mousePressEvent(self, event):
        self.clicked.emit(event)

    def hoverEnterEvent(self, event):
        self.hoverEnter.emit(event)

    def hoverLeaveEvent(self, event):
        self.hoverLeave.emit(event)

    def mouseMoveEvent(self, event):
        self.mouseMove.emit(event)

    def updateGeometry(self, rect):
        self.prepareGeometryChange()
        self._rect = rect
        self.update()

    def updateColor(self, color):
        self._color = color
        self.update()

    @property
    def direction(self):
        return self._direction
