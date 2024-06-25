from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import PatternDecoder


class QuestObjectiveDiscoverSubArea(QuestObjective, IDataCenter):

    _subArea: SubArea = None

    _text: str = None

    def __init__(self):
        super().__init__()

    @property
    def subAreaId(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter0

    @property
    def subArea(self) -> SubArea:
        if not self._subArea:
            self._subArea = SubArea.getSubAreaById(self.subAreaId)
        return self._subArea

    @property
    def text(self) -> str:
        if not self._text:
            self._text = PatternDecoder.getDescription(self.type.name, [self.subArea.name])
        return self._text
