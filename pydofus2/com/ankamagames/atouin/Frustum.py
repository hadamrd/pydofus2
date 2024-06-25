from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.DofusUI.StageShareManager import StageShareManager


class Frustum:
    MAX_WIDTH = AtouinConstants.MAP_WIDTH * AtouinConstants.CELL_WIDTH + AtouinConstants.CELL_HALF_WIDTH
    MAX_HEIGHT = AtouinConstants.MAP_HEIGHT * AtouinConstants.CELL_HEIGHT + AtouinConstants.CELL_HALF_HEIGHT
    RATIO = MAX_WIDTH / MAX_HEIGHT

    def __init__(self, marginLeft=0, marginTop=0, marginRight=0, marginBottom=0):
        self._marginTop = marginTop
        self._marginRight = marginRight
        self._marginBottom = marginBottom
        self._marginLeft = marginLeft
        self.scale = 1.0
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.refresh()

    @property
    def marginLeft(self):
        return self._marginLeft

    @property
    def marginRight(self):
        return self._marginRight

    @property
    def marginTop(self):
        return self._marginTop

    @property
    def marginBottom(self):
        return self._marginBottom

    def refresh(self):
        self.scale = StageShareManager().startHeight / (self.MAX_HEIGHT + self._marginTop + self._marginBottom)
        self.width = self.MAX_WIDTH * self.scale
        self.height = self.MAX_HEIGHT * self.scale

        currentRatio = self.width / self.height
        if currentRatio < self.RATIO:
            self.height = self.width / self.RATIO
        elif currentRatio > self.RATIO:
            self.width = self.height * self.RATIO

        xSpace = StageShareManager().startWidth - self.MAX_WIDTH * self.scale + self._marginLeft - self._marginRight
        ySpace = StageShareManager().startHeight - self.MAX_HEIGHT * self.scale + self._marginTop - self._marginBottom

        if (self._marginLeft is not None and self._marginLeft != 0) and self._marginRight is not None:
            divX = (self._marginLeft + self._marginRight) / self._marginLeft
        elif self._marginLeft:
            divX = 2 + xSpace / self._marginLeft
        elif self._marginRight is not None and self._marginRight != 0:
            divX = 2 - xSpace / self._marginRight
        else:
            divX = 2

        if (self._marginTop is not None and self._marginTop != 0) and self._marginBottom is not None:
            divY = (self._marginTop + self._marginBottom) / self._marginTop
        elif self._marginTop:
            divY = 2 + ySpace / self._marginTop
        elif self._marginBottom:
            divY = ySpace / self._marginBottom - 2
        else:
            divY = 2

        self.x = xSpace / divX
        self.y = ySpace / divY

    @property
    def bottom(self):
        return self.y + self.height + self._marginRight + self._marginLeft

    @property
    def top(self):
        return self.y

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width + self._marginLeft + self._marginRight

    def __str__(self):
        return f"Frustum: x={self.x}, y={self.y}, width={self.width}, height={self.height}, scale={self.scale}"
