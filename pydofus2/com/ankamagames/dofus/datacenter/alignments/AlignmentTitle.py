from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData


class AlignmentTitle:
    MODULE = "AlignmentTitles"

    sideId: int

    namesId: list[int]

    shortsId: list[int]

    @classmethod
    def getAlignmentTitles(cls) -> list["AlignmentTitle"]:
        return GameData().getObjects(cls.MODULE)

    @classmethod
    def getAlignmentTitleById(cls, id) -> "AlignmentTitle":
        return GameData().getObject(cls.MODULE, id)

    idAccessors = IdAccessors(getAlignmentTitleById, getAlignmentTitles)
