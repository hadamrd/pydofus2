from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsItemGroup

from pydofus2.com.ankamagames.atouin.Frustum import Frustum
from pydofus2.com.ankamagames.atouin.FrustumShape import FrustumShape
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import DirectionsEnum
from pydofus2.DofusUI.StageShareManager import StageShareManager


class SingletonError(Exception):
    pass


class FrustumManager(metaclass=Singleton):
    SHAPE_INSIDE_PADDING = 30  # Example padding value

    def __init__(self):
        super().__init__()

    def init(self, frustumContainer: QGraphicsItemGroup):
        self._frustumContainer = frustumContainer
        self._shapeTop = FrustumShape(DirectionsEnum.UP)
        self._shapeRight = FrustumShape(DirectionsEnum.RIGHT)
        self._shapeBottom = FrustumShape(DirectionsEnum.DOWN)
        self._shapeLeft = FrustumShape(DirectionsEnum.LEFT)

        self._frustumContainer.addToGroup(self._shapeLeft)
        self._frustumContainer.addToGroup(self._shapeTop)
        self._frustumContainer.addToGroup(self._shapeRight)
        self._frustumContainer.addToGroup(self._shapeBottom)

        # Connecting signals to slots for interaction
        self._shapeLeft.clicked.connect(self.click)
        self._shapeTop.clicked.connect(self.click)
        self._shapeRight.clicked.connect(self.click)
        self._shapeBottom.clicked.connect(self.click)

        self._shapeLeft.hoverEnter.connect(self.mouseMove)
        self._shapeTop.hoverEnter.connect(self.mouseMove)
        self._shapeRight.hoverEnter.connect(self.mouseMove)
        self._shapeBottom.hoverEnter.connect(self.mouseMove)

        self._shapeLeft.hoverLeave.connect(self.out)
        self._shapeTop.hoverLeave.connect(self.out)
        self._shapeRight.hoverLeave.connect(self.out)
        self._shapeBottom.hoverLeave.connect(self.out)

        self._shapeLeft.mouseMove.connect(self.mouseMove)
        self._shapeTop.mouseMove.connect(self.mouseMove)
        self._shapeRight.mouseMove.connect(self.mouseMove)
        self._shapeBottom.mouseMove.connect(self.mouseMove)

        self.setBorderInteraction(False)
        self._lastCellId = -1

    def setBorderInteraction(self, enable):
        # Logic to enable or disable interaction at the border
        pass

    def click(self, event):
        print("Clicked on", event.sender())

    def mouseMove(self, event):
        print("Mouse over", event.sender())

    def out(self, event):
        print("Mouse out from", event.sender())

    def getShape(self, direction):
        direction = DirectionsEnum(direction)
        if direction == DirectionsEnum.UP:
            return self._shapeTop
        elif direction == DirectionsEnum.LEFT:
            return self._shapeLeft
        elif direction == DirectionsEnum.RIGHT:
            return self._shapeRight
        elif direction == DirectionsEnum.DOWN:
            return self._shapeBottom
        return None

    @property
    def frustum(self):
        return self._frustrum

    @frustum.setter
    def frustum(self, rFrustum: Frustum):
        self._frustrum = rFrustum
        self._draw_shapes()

    def _draw_shapes(self):
        color = QColor(0)
        color.setAlphaF(1)
        new_rect_left = QRectF(self.SHAPE_INSIDE_PADDING, 0, -512, StageShareManager().startHeight)
        self._shapeLeft.updateGeometry(new_rect_left)
        self._shapeLeft.updateColor(color)  # Black color with full opacity

        # Update properties for _shapeRight
        new_rect_right = QRectF(
            StageShareManager().startWidth - self.SHAPE_INSIDE_PADDING, 0, 512, StageShareManager().startHeight
        )
        self._shapeRight.updateGeometry(new_rect_right)
        self._shapeRight.updateColor(color)

        # Drawing for _shapeTop
        new_rect_top = QRectF(
            self.SHAPE_INSIDE_PADDING,
            self.SHAPE_INSIDE_PADDING - 13,
            StageShareManager().startWidth - self.SHAPE_INSIDE_PADDING * 2,
            -512,
        )
        self._shapeTop.updateColor(color)
        self._shapeTop.updateGeometry(new_rect_top)

        # Drawing for _shapeBottom
        new_rect_bot = QRectF(
            self.SHAPE_INSIDE_PADDING,
            int(self._frustrum.bottom - self.SHAPE_INSIDE_PADDING / 2 - 5),
            int(StageShareManager().startWidth - self.SHAPE_INSIDE_PADDING * 2),
            int(self._frustrum.marginBottom + self.SHAPE_INSIDE_PADDING * 2),
        )
        self._shapeBottom.updateColor(color)
        self._shapeBottom.updateGeometry(new_rect_bot)
