from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsItem

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class FurnitureZoneTile(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self._displayBehaviors = None
        self._displayed = False
        self._currentCell = None
        self._cellId = 0
        self.strata = 10
        self.needFill = False
        self.offset = QPointF()

    def display(self, strata=0):
        EntitiesDisplayManager().displayEntity(self, MapPoint.fromCellId(self._cellId), strata, False)
        self._displayed = True
        if self.offset:
            self.setPos(self.x() - self.offset.x(), self.y() - self.offset.y())

    def draw(self, bottomLeft, topLeft, topRight, bottomRight, cellHeight):
        painter = QPainter(self)
        cellHeight *= -1
        white = QColor(255, 255, 255)

        # Setting initial conditions for drawing
        if cellHeight:
            painter.setPen(QPen(white, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.setOpacity(0.8)

            # Initial vertical line
            painter.drawLine(
                QPointF(AtouinConstants.CELL_HALF_WIDTH, 0), QPointF(AtouinConstants.CELL_HALF_WIDTH, cellHeight)
            )
            # Horizontal line from center to top
            painter.drawLine(
                QPointF(0, AtouinConstants.CELL_HALF_HEIGHT), QPointF(0, cellHeight + AtouinConstants.CELL_HALF_HEIGHT)
            )
            # Left slant line from center
            painter.drawLine(
                QPointF(-AtouinConstants.CELL_HALF_WIDTH, 0), QPointF(-AtouinConstants.CELL_HALF_WIDTH, cellHeight)
            )
            # Triangle base
            painter.drawLine(QPointF(-AtouinConstants.CELL_HALF_WIDTH, 0), QPointF(AtouinConstants.CELL_HALF_WIDTH, 0))

        # Fill condition based on `needFill`
        if self.needFill:
            painter.setBrush(QColor(255, 255, 255, 204))  # white with opacity
            painter.setPen(QPen(Qt.NoPen))  # No border for fill

        # Drawing top-right line conditionally
        painter.setPen(QPen(white, 2, Qt.SolidLine))
        if not topRight or self.needFill:
            painter.setOpacity(0.8)
        else:
            painter.setOpacity(0)
        painter.drawLine(
            QPointF(0, cellHeight - AtouinConstants.CELL_HALF_HEIGHT),
            QPointF(AtouinConstants.CELL_HALF_WIDTH, cellHeight),
        )

        # Drawing bottom-right line conditionally
        if not bottomRight or self.needFill:
            painter.setOpacity(0.8)
        else:
            painter.setOpacity(0)
        painter.drawLine(
            QPointF(AtouinConstants.CELL_HALF_WIDTH, cellHeight),
            QPointF(0, cellHeight + AtouinConstants.CELL_HALF_HEIGHT),
        )

        # Drawing bottom-left line conditionally
        if not bottomLeft or self.needFill:
            painter.setOpacity(0.8)
        else:
            painter.setOpacity(0)
        painter.drawLine(
            QPointF(0, cellHeight + AtouinConstants.CELL_HALF_HEIGHT),
            QPointF(-AtouinConstants.CELL_HALF_WIDTH, cellHeight),
        )

        # Drawing top-left line conditionally
        if not topLeft or self.needFill:
            painter.setOpacity(0.8)
        else:
            painter.setOpacity(0)
        painter.drawLine(
            QPointF(-AtouinConstants.CELL_HALF_WIDTH, cellHeight),
            QPointF(0, cellHeight - AtouinConstants.CELL_HALF_HEIGHT),
        )

        # End the filling if needed
        if self.needFill:
            painter.endFill()

        painter.end()

    def remove(self):
        self.offset = QPointF()
        self.needFill = False
        self._displayed = False
        EntitiesDisplayManager().removeEntity(self)

    @property
    def displayBehaviors(self):
        return self._displayBehaviors

    @displayBehaviors.setter
    def displayBehaviors(self, value):
        self._displayBehaviors = value

    @property
    def currentCell(self):
        return self._currentCell

    @currentCell.setter
    def currentCell(self, value):
        self._currentCell = value

    @property
    def displayed(self):
        return self._displayed

    @property
    def absoluteBounds(self):
        return self._displayBehaviors.getAbsoluteBounds(self)

    @property
    def cellId(self):
        return self._cellId

    @cellId.setter
    def cellId(self, value):
        self._cellId = value

    def boundingRect(self):
        return QRectF(0, 0, 100, 100)  # Example dimensions

    def paint(self, painter, option, widget=None):
        self.draw(True, True, True, True, 20)  # Example usage within paint, assuming conditions are met
