from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.data.IPostInit import IPostInit
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class HintCategory(IDataCenter, IPostInit):

    MODULE: str = "Hints"

    _allHints: list = None
    id: int
    nameId: int
    _name: str = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getHintCategoryById(cls, id: int) -> "HintCategory":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getHintCategories(cls) -> list["HintCategory"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def name(self):
        if self._name is None:
            self._name = I18n.getText(self.nameId)
        return self._name
