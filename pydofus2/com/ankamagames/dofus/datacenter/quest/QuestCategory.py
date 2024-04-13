from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.quest.Quest import Quest


class QuestCategory(IDataCenter):

    MODULE: str = "QuestCategory"

    id: int

    nameId: int

    order: int

    questIds: list[int]

    _name: str = None

    _quests: list["Quest"] = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getQuestCategoryById(cls, id: int) -> "QuestCategory":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getQuestCategories(cls) -> list["QuestCategory"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def quests(self) -> list["Quest"]:
        from pydofus2.com.ankamagames.dofus.datacenter.quest.Quest import Quest

        if not self._quests:
            self._quests = [Quest.getQuestById(qid) for qid in self.questIds]
        return self._quests

    idAccessors: IdAccessors = IdAccessors(getQuestCategoryById, getQuestCategories)
