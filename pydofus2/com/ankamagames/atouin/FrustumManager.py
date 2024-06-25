from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor

from pydofus2.com.ankamagames.atouin.Frustum import Frustum
from pydofus2.com.ankamagames.atouin.FrustumShape import FrustumShape
from pydofus2.com.ankamagames.atouin.types.SimpleGraphicsContainer import SimpleGraphicsContainer
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import DirectionsEnum
from pydofus2.DofusUI.StageShareManager import StageShareManager


class FrustumManager(metaclass=Singleton):
    SHAPE_INSIDE_PADDING = 30  # Example padding value

    def __init__(self):
        super().__init__()

    def init(self, frustumContainer: SimpleGraphicsContainer):
        self._frustumContainer = frustumContainer
        self._shapeTop = FrustumShape(DirectionsEnum.UP)
        self._shapeRight = FrustumShape(DirectionsEnum.RIGHT)
        self._shapeBottom = FrustumShape(DirectionsEnum.DOWN)
        self._shapeLeft = FrustumShape(DirectionsEnum.LEFT)
        shapes = [self._shapeTop, self._shapeRight, self._shapeBottom, self._shapeLeft]
        for shape in shapes:
            self._frustumContainer.addChild(shape)
            shape.clicked.connect(lambda e, shape=shape: self.click(e, shape))
            shape.hoverEnter.connect(lambda e, shape=shape: self.mouseMove(e, shape))
            shape.hoverLeave.connect(lambda e, shape=shape: self.out(e, shape))
            shape.mouseMove.connect(lambda e, shape=shape: self.mouseMove(e, shape))
        self.setBorderInteraction(False)
        self._lastCellId = -1

    def setBorderInteraction(self, enable):
        # Logic to enable or disable interaction at the border
        ...

    def click(self, event: Frustum, shape: FrustumShape):
        ...

    def mouseMove(self, event, shape: FrustumShape):
        ...

    def out(self, event: Frustum, shape: FrustumShape):
        ...

    def getShape(self, direction):
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
    def frustum(self) -> Frustum:
        return self._frustum

    @frustum.setter
    def frustum(self, rFrustum: Frustum):
        self._frustum = rFrustum
        self._drawShapes()

    def _drawShapes(self):
        color = QColor("blue")
        color.setAlphaF(0)
        # Drawing for shapeLeft
        new_rect_left = QRectF(self.SHAPE_INSIDE_PADDING, 0, -512, StageShareManager().startHeight)
        self._shapeLeft.updateGeometry(new_rect_left)
        self._shapeLeft.updateColor(color)
        # Drawing for shapeRight
        new_rect_right = QRectF(
            StageShareManager().startWidth - self.SHAPE_INSIDE_PADDING, 0, 512, StageShareManager().startHeight
        )
        self._shapeRight.updateGeometry(new_rect_right)
        self._shapeRight.updateColor(color)
        # Drawing for shapeTop
        new_rect_top = QRectF(
            self.SHAPE_INSIDE_PADDING,
            self.SHAPE_INSIDE_PADDING - 13,
            StageShareManager().startWidth - self.SHAPE_INSIDE_PADDING * 2,
            -512,
        )
        self._shapeTop.updateColor(color)
        self._shapeTop.updateGeometry(new_rect_top)
        # Drawing for shapeBottom
        new_rect_bot = QRectF(
            self.SHAPE_INSIDE_PADDING,
            self.frustum.bottom - self.SHAPE_INSIDE_PADDING / 2 - 5,
            StageShareManager().startWidth - self.SHAPE_INSIDE_PADDING * 2,
            self.frustum.marginBottom + self.SHAPE_INSIDE_PADDING * 2,
        )
        self._shapeBottom.updateColor(color)
        self._shapeBottom.updateGeometry(new_rect_bot)
