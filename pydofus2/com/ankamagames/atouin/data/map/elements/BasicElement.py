from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
from pydofus2.com.ankamagames.atouin.enums.ElementTypesEnum import \
    ElementTypesEnum
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import \
    ByteArray


class BasicElement:

    _cell: Cell

    def __init__(self, cell: Cell):
        self._cell = cell

    @classmethod
    def getElementFromType(cls, type: int, cell: Cell) -> "BasicElement":
        from pydofus2.com.ankamagames.atouin.data.map.elements.GraphicalElement import \
            GraphicalElement
        from pydofus2.com.ankamagames.atouin.data.map.elements.SoundElement import \
            SoundElement

        if type == ElementTypesEnum.GRAPHICAL:
            return GraphicalElement(cell)
        if type == ElementTypesEnum.SOUND:
            return SoundElement(cell)
        else:
            raise Exception(
                "Un �l�ment de type inconnu " + str(type) + " a �t� trouv� sur la cellule " + str(cell.cellId) + "!"
            )

    @property
    def cell(self) -> Cell:
        return self._cell

    @property
    def elementType(self) -> int:
        return NotImplementedError

    def fromRaw(self, raw: ByteArray, mapVersion: int) -> None:
        raise NotImplementedError
