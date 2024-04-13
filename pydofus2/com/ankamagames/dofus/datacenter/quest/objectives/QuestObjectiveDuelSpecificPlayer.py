from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import PatternDecoder


class QuestObjectiveDuelSpecificPlayer(QuestObjective, IDataCenter):

    _specificPlayerText: str

    _text: str

    def __init__(self):
        super().__init__()

    @property
    def specificPlayerTextId(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter0

    @property
    def specificPlayerText(self) -> str:
        if not self._specificPlayerText:
            self._specificPlayerText = I18n.getText(self.specificPlayerTextId)
        return self._specificPlayerText

    @property
    def text(self) -> str:
        if not self._text:
            self._text = PatternDecoder.getDescription(self.type.name, [self.specificPlayerText])
        return self._text
