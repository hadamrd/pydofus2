from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import PatternDecoder


class QuestObjectiveCraftItem(QuestObjective, IDataCenter):

    _item: Item

    _text: str

    def __init__(self):
        super().__init__()

    @property
    def itemId(self) -> int:
        if not self.parameters or self.parameters.numParams < 2:
            return 0
        return self.parameters.parameter0

    @property
    def item(self) -> Item:
        if not self._item:
            self._item = Item.getItemById(self.itemId)
        return self._item

    @property
    def quantity(self) -> int:
        if not self.parameters or self.parameters.numParams < 2:
            return 0
        return self.parameters.parameter1

    @property
    def text(self) -> str:
        if not self._text:
            self._text = PatternDecoder.getDescription(
                self.type.name, ["{item," + str(self.itemId) + "}", self.quantity]
            )
        return self._text
