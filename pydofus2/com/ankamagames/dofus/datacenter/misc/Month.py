from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class Month(IDataCenter):
    MODULE = "Months"

    def __init__(self):
        self.id: int = None
        self.nameId = None
        self._name = ""

    @property
    def name(self):
        if self._name == "":
            self._name = I18n.getText(self.nameId)
        return self._name

    @classmethod
    def getMonthById(cls, id: int) -> "Month":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getMonths(cls) -> list["Month"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors = IdAccessors(getMonthById, getMonths)
