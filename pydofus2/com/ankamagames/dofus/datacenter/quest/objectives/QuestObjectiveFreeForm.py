from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class QuestObjectiveFreeForm(QuestObjective, IDataCenter):

    _freeFormText: str = None

    def __init__(self):
        super().__init__()

    @property
    def freeFormTextId(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter0

    @property
    def freeFormText(self) -> str:
        if not self._freeFormText:
            self._freeFormText = I18n.getText(self.freeFormTextId)
        return self._freeFormText

    @property
    def text(self) -> str:
        return self.freeFormText
