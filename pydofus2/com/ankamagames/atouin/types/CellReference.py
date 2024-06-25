from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsItem


class CellReference:
    def __init__(self, nId):
        self.id = nId
        self.listSprites = list[QGraphicsItem]()
        self.gfxId = []
        self.elevation = 0
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.mov = False
        self.isDisabled = False
        self.rendered = False
        self._visible = True
        self._lock = False

    def addSprite(self, d):
        self.listSprites.append(d)

    def addGfx(self, nGfxId):
        self.gfxId.append(nGfxId)

    def lock(self):
        self._lock = True

    @property
    def locked(self):
        return self._lock

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, bValue):
        if self._visible != bValue:
            self._visible = bValue
            for sprite in self.listSprites:
                sprite.setVisible(bValue)

    def bounds(self):
        # Assuming QRectF usage for PyQt5
        from PyQt5.QtCore import QRectF

        rect = QRectF()
        for sprite in self.listSprites:
            rect = rect.united(sprite.sceneBoundingRect())
        return rect

    def getAvgColor(self):
        red, green, blue = 0, 0, 0
        len_sprites = len(self.listSprites)
        for sprite in self.listSprites:
            color = sprite.pen().color() if hasattr(sprite, "pen") else QColor(255, 255, 255)  # Default to white
            red += color.red()
            green += color.green()
            blue += color.blue()
        if len_sprites > 0:
            red = int(red / len_sprites)
            green = int(green / len_sprites)
            blue = int(blue / len_sprites)
        return (red << 16) | (green << 8) | blue
