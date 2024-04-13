from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.datacenter.npcs.Npc import Npc
from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import PatternDecoder


class QuestObjectiveBringSoulToNpc(QuestObjective, IDataCenter):

    _npc: Npc = None

    _monster: Monster = None

    _text: str = ""

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
    def monsterId(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter1

    @property
    def monster(self) -> Monster:
        if not self._monster:
            self._monster = Monster.getMonsterById(self.monsterId)
        return self._monster

    @property
    def quantity(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter2

    @property
    def text(self) -> str:
        if not self._text:
            self._text = PatternDecoder.getDescription(
                self.type.name, [self.npc.name, self.monster.name, self.quantity]
            )
        return self._text
