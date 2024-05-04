from PyQt5.QtCore import QRectF, Qt, pyqtProperty
from PyQt5.QtGui import QBrush, QColor, QCursor, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)


class Sprite(QGraphicsObject):
    def __init__(self):
        super(Sprite, self).__init__()
        self._background = QGraphicsRectItem(self)
        self._background.setBrush(QColor("transparent"))
        self._background.setZValue(-1)
        self._background.setPen(QPen(Qt.NoPen))
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        self._mouseEnabled = True
        self._mouseChildren = True
        self._buttonMode = False
        self._cacheAsBitmap = False
        self._cachedPixmap = None
        self._needs_update = False
        self.name = ""

    def boundingRect(self):
        rect = QRectF()
        for child in self.childItems():
            if child == self._background:
                continue
            rect = rect.united(child.boundingRect().translated(child.pos()))
        self._background.setRect(rect)
        return rect

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Sprite clicked! Let's do something cool!")
        super().mousePressEvent(event)

    def addChild(self, item: QGraphicsItem):
        item.setParentItem(self)

    def removeChild(self, item: QGraphicsItem):
        if item.parentItem() == self:
            item.setParentItem(None)

    @pyqtProperty(bool)
    def mouseEnabled(self):
        return self._mouseEnabled

    @mouseEnabled.setter
    def mouseEnabled(self, value):
        self._mouseEnabled = value
        if value:
            self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        else:
            self.setAcceptedMouseButtons(Qt.NoButton)

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self._background.brush().color()

    @backgroundColor.setter
    def backgroundColor(self, color):
        self._background.setBrush(QBrush(QColor(color)))

    def mousePressEvent(self, event):
        if not self._mouseEnabled:
            event.ignore()
        else:
            super().mousePressEvent(event)

    def updateBoundingRect(self):
        self.prepareGeometryChange()
        self.boundingRect()

    @pyqtProperty(bool)
    def mouseChildren(self):
        return self._mouseChildrenEnabled

    @mouseChildren.setter
    def mouseChildren(self, value):
        self._mouseChildrenEnabled = value
        for child in self.childItems():
            child.setAcceptedMouseButtons(Qt.LeftButton if value else Qt.NoButton)
            child.setAcceptHoverEvents(value)

    @pyqtProperty(bool)
    def buttonMode(self):
        return self._buttonMode

    @buttonMode.setter
    def buttonMode(self, enabled):
        self._buttonMode = enabled
        # Change cursor appearance based on the button mode state
        if enabled:
            self.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            self.unsetCursor()

    def hoverEnterEvent(self, event):
        if self._buttonMode:
            self.setCursor(QCursor(Qt.PointingHandCursor))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self._buttonMode:
            self.unsetCursor()
        super().hoverLeaveEvent(event)

    @pyqtProperty(bool)
    def cacheAsBitmap(self):
        return self._cacheAsBitmap

    @cacheAsBitmap.setter
    def cacheAsBitmap(self, value):
        self._cacheAsBitmap = value
        if value:
            self._updateCache()

    def _updateCache(self):
        """Updates the cached pixmap."""
        rect = self.boundingRect()
        if rect:
            self._cached_pixmap = QPixmap(rect.size().toSize())
            self._cached_pixmap.fill(Qt.transparent)
            cache_painter = QPainter(self._cached_pixmap)
            cache_painter.setRenderHint(QPainter.Antialiasing)  # Optional for smoother rendering
            cache_painter.setClipping(True)  # Clip to bounding rect
            cache_painter.setClipRect(rect)
            # Paint the background first
            cache_painter.fillRect(rect, self._background.brush())
            # Custom painting logic for child items if any
            self._needs_update = False
            cache_painter.end()
            print("cached pixmap created")


def main():
    import sys

    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    sprite = Sprite()
    sprite.backgroundColor = "lightblue"  # Set a visible background color
    sprite.buttonMode = True  # Enable hand cursor on hover
    # sprite.cacheAsBitmap = True  # Enable caching as bitmap

    rect1 = QGraphicsRectItem(0, 0, 100, 100)
    rect1.setBrush(QBrush(QColor("red")))
    rect1.setFlag(QGraphicsRectItem.ItemIsMovable, True)  # Make the rectangle inside sprite movable
    sprite.addChild(rect1)

    rect2 = QGraphicsRectItem(150, 150, 100, 100)
    rect2.setBrush(QBrush(QColor("green")))
    sprite.addChild(rect2)

    scene.addItem(sprite)
    view = QGraphicsView(scene)
    view.setSceneRect(0, 0, 400, 400)
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
