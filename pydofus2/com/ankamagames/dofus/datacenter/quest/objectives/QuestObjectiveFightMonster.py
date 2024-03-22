from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import \
    QuestObjective
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class QuestObjectiveFightMonster(QuestObjective, IDataCenter):

    _text: str = None

    def __init__(self):
        super().__init__()

    @property
    def monsterId(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter0
    
    @property
    def quantity(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter1

    @property
    def dungeonOnly(self) -> bool:
        if not self.parameters:
            return False
        return self.parameters.dungeonOnly

    @property
    def text(self) -> str:
        return f"{{chatmonster,{self.monsterId}}}"
