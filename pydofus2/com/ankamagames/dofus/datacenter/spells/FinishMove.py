from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import SpellLevel
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class FinishMove(IDataCenter):

    MODULE: str = "FinishMoves"
    id: int

    duration: int

    free: bool

    nameId: int

    category: int

    spellLevel: int

    _name: str

    def __init__(self):
        super().__init__()

    @classmethod
    def getFinishMoveById(cls, id: int) -> "FinishMove":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getFinishMoves(cls) -> list["FinishMove"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    def getSpellLevel(self) -> SpellLevel:
        return SpellLevel.getLevelById(self.spellLevel)

    idAccessors: IdAccessors = IdAccessors(getFinishMoveById, getFinishMoves)
