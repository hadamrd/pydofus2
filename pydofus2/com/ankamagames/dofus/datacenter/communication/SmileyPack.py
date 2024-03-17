from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class SmileyPack(IDataCenter):

    MODULE: str = "SmileyPacks"

    id: int

    nameId: int

    order: int

    smileys: list[int]

    _name: str = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getSmileyPackById(cls, id: int) -> "SmileyPack":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getSmileyPacks(cls) -> list["SmileyPack"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    idAccessors: IdAccessors = IdAccessors(getSmileyPackById, getSmileyPacks)
