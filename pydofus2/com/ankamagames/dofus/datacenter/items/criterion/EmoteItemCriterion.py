from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class EmoteItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    def getEmotesList(self) -> list:
        emoticonFrame: EmoticonFrame = Kernel().worker.getFrame("EmoticonFrame")
        if emoticonFrame:
            return emoticonFrame.emotesList
        return None

    @property
    def isRespected(self) -> bool:
        emoteWrapper: EmoteWrapper = None
        for emoteWrapper in self.getEmotesList():
            if emoteWrapper.emote.id == self._criterionValue:
                return False
        return True

    @property
    def text(self) -> str:
        readableCriterion: str = I18n.getUiText("ui.tooltip.possessEmote")
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterion = I18n.getUiText("ui.tooltip.dontPossessEmote")
        return readableCriterion + " '" + Emoticon.getEmoticonById(self._criterionValue).name + "'"

    def clone(self) -> IItemCriterion:
        return EmoteItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        id: int = 0
        for id in self.getEmotesList():
            if id == self._criterionValue:
                return 1
        return 0
