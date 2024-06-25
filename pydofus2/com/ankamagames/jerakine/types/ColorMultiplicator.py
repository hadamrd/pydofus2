class ColorMultiplicator:
    red: float

    green: float

    blue: float

    _isOne: bool

    def __init__(
        self,
        redComponent: int,
        greenComponent: int,
        blueComponent: int,
        forceCalculation: bool = False,
    ):
        super().__init__()
        self.red = redComponent
        self.green = greenComponent
        self.blue = blueComponent
        if not forceCalculation and redComponent + greenComponent + blueComponent == 0:
            self._isOne = True
        else:
            self._isOne = False

    @staticmethod
    def clamp(value: float, min: float, max: float) -> float:
        if value > max:
            return max
        if value < min:
            return min
        return value

    def isOne(self) -> bool:
        return self._isOne

    def multiply(self, cm: "ColorMultiplicator") -> "ColorMultiplicator":
        if self._isOne:
            return cm
        if cm.isOne():
            return self
        cmr: ColorMultiplicator = ColorMultiplicator(0, 0, 0)
        cmr.red = self.red + cm.red
        cmr.green = self.green + cm.green
        cmr.blue = self.blue + cm.blue
        cmr.red = self.clamp(cmr.red, -128, 127)
        cmr.green = self.clamp(cmr.green, -128, 127)
        cmr.blue = self.clamp(cmr.blue, -128, 127)
        cmr._isOne = False
        return cmr

    def __str__(self) -> str:
        return f"[r: {self.red}, g: {self.green} , b: {self.blue}]"
