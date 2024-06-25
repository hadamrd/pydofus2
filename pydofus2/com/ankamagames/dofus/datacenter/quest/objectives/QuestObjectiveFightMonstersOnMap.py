from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import PatternDecoder


class QuestObjectiveFightMonstersOnMap(QuestObjective, IDataCenter):

    _monster: Monster = None

    _mapDescriptionText: str = ""

    _text: str = ""

    def __init__(self):
        super().__init__()

    @property
    def monsterId(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter0

    @property
    def monster(self) -> Monster:
        if not self._monster:
            self._monster = Monster.getMonsterById(self.monsterId)
        return self._monster

    @property
    def quantity(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter1

    @property
    def mapDescriptionTextId(self) -> int:
        if not self.parameters:
            return 0
        return self.parameters.parameter3

    @property
    def mapDescriptionText(self) -> str:
        if not self._mapDescriptionText:
            self._mapDescriptionText = I18n.getText(self.mapDescriptionTextId)
        return self._mapDescriptionText

    @property
    def text(self) -> str:
        if not self._text:
            self._text = PatternDecoder.getDescription(
                self.type.name, ["{chatmonster," + str(self.monsterId) + "}", self.quantity, self.mapDescriptionText]
            )
        return self._text
