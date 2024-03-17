from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class QuestObjectiveType(IDataCenter):

    MODULE: str = "QuestObjectiveTypes"

    id: int

    nameId: int

    _name: str = ""

    def __init__(self):
        super().__init__()

    @classmethod
    def getQuestObjectiveTypeById(cls, id: int) -> "QuestObjectiveType":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getQuestObjectiveTypes(cls) -> list["QuestObjectiveType"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    idAccessors: IdAccessors = IdAccessors(getQuestObjectiveTypeById, getQuestObjectiveTypes)
