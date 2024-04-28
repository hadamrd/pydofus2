class CellContainer:
    _ratio = None  # Presuming this should be a class variable as in ActionScript

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
