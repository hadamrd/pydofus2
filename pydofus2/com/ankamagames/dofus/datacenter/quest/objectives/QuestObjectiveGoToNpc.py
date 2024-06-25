from pydofus2.com.ankamagames.dofus.datacenter.npcs.Npc import Npc
from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import PatternDecoder


class QuestObjectiveGoToNpc(QuestObjective, IDataCenter):

    _npc: Npc

    _text: str

    def __init__(self):
        super().__init__()

    @property
    def npcId(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter0

    @property
    def npc(self) -> Npc:
        if not self._npc:
            self._npc = Npc.getNpcById(self.npcId)
        return self._npc

    @property
    def text(self) -> str:
        if not self._text:
            self._text = PatternDecoder.getDescription(self.type.name, [self.npc.name])
        return self._text
