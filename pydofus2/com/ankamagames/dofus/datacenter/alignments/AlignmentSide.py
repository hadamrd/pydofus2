from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n


class AlignmentSide:
    MODULE = "AlignmentSides"

    id: int

    nameId: int

    _name: str = None

    @classmethod
    def getAlignmentSides(cls) -> list["AlignmentSide"]:
        return GameData().getObjects(cls.MODULE)

    @classmethod
    def getAlignmentSideById(cls, id) -> "AlignmentSide":
        return GameData().getObject(cls.MODULE, id)

    @property
    def name(self):
        if self._name is None:
            self._name = I18n.getText(self.nameId)
        return self._name

    idAccessors = IdAccessors(getAlignmentSideById, getAlignmentSides)
