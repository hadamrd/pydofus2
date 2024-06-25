from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class SpellPair(IDataCenter):

    MODULE: str = "SpellPairs"

    id: int

    nameId: int

    descriptionId: int

    iconId: int

    _name: str = None

    _desc: str = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getSpellPairById(cls, id: int) -> "SpellPair":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getSpellPairs(cls) -> list["SpellPair"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def description(self) -> str:
        if not self._desc:
            self._desc = I18n.getText(self.descriptionId)
        return self._desc
