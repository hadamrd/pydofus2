from types import FunctionType

from pydofus2.com.ankamagames.jerakine.interfaces.ICustomUnicNameGetter import ICustomUnicNameGetter


class GraphicCell(ICustomUnicNameGetter):

    _dropValidator: FunctionType

    _removeDropSource: FunctionType

    _processDrop: FunctionType

    _name: str

    cellId: int

    _initialElevation: int = 0

    def __init__(self, cellId: int):
        self._dropValidator = self.returnTrueFunctionType
        self._removeDropSource = self.returnTrueFunctionType
        self._processDrop = self.returnTrueFunctionType
        super().__init__()
        self.cellId = cellId
        str(cellId)
        self._name = "cell::" + cellId

    @property
    def dropValidator(self) -> FunctionType:
        return self._dropValidator

    @dropValidator.setter
    def dropValidator(self, dv: FunctionType) -> None:
        self._dropValidator = dv

    @property
    def customUnicName(self) -> str:
        return self._name

    @property
    def removeDropSource(self) -> FunctionType:
        return self._removeDropSource

    @removeDropSource.setter
    def removeDropSource(self, rds: FunctionType) -> None:
        self._removeDropSource = rds

    @property
    def processDrop(self) -> FunctionType:
        return self._processDrop

    @processDrop.setter
    def processDrop(self, pd: FunctionType) -> None:
        self._processDrop = pd

    @property
    def initialElevation(self) -> int:
        return self._initialElevation

    @initialElevation.setter
    def initialElevation(self, value: int) -> None:
        self._initialElevation = value

    def returnTrueFunctionType(self, *args) -> bool:
        return True
