from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance
from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.StorageOptionManager import StorageOptionManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.inventoryView.StorageGenericView import StorageGenericView
from pydofus2.com.ankamagames.dofus.types.enums.ItemCategoryEnum import ItemCategoryEnum
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n


class BankMinoukiView(StorageGenericView):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "bankMinouki"

    def isListening(self, item: ItemWrapper) -> bool:
        return (
            super().isListening(item)
            and item.category == ItemCategoryEnum.RESOURCES_CATEGORY
            and item.typeId == ItemCategoryEnum.ECAFLIP_CARD_CATEGORY
        )

    def updateView(self) -> None:
        super().updateView()

    def addItem(self, item: ItemWrapper, invisible: int, needUpdateView: bool = True) -> None:
        type: int = 0
        clone: ItemWrapper = item.clone()
        clone.quantity -= invisible
        self._content.unshift(clone)
        if self._sortedContent:
            self._sortedContent.unshift(clone)
        cardTypes: list = self.getMinoukiCardTypes(item)
        for type in cardTypes:
            if self._typesQty[type] and self._typesQty[type] > 0:
                self._typesQty[type] += 1
            else:
                self._typesQty[type] = 1
                self._types[type] = {
                    "name": I18n.getUiText("ui.customEffect." + type),
                    "id": type,
                }
        if needUpdateView:
            self.updateView()

    def removeItem(self, item: ItemWrapper, invisible: int) -> None:
        effect: EffectInstance = None
        idx: int = self.getItemIndex(item)
        if idx == -1:
            return
        for effect in item.possibleEffects:
            if effect.effectId == ActionIds.ACTION_ITEM_CUSTOM_EFFECT:
                if self._typesQty[effect.parameter2] and self._typesQty[effect.parameter2] > 0:
                    self._typesQty[effect.parameter2] -= 1
                    if self._typesQty[effect.parameter2] == 0:
                        del self._types[effect.parameter2]
        self._content.remove(idx)
        if self._sortedContent:
            idx = self.getItemIndex(item, self._sortedContent)
            if idx != -1:
                self._sortedContent.remove(idx)
        self.updateView()

    def getMinoukiCardTypes(self, item: ItemWrapper) -> list:
        effect: EffectInstance = None
        types: list = []
        for effect in item.possibleEffects:
            if effect.effectId == ActionIds.ACTION_ITEM_CUSTOM_EFFECT:
                types.append(effect.parameter2)
        return types

    def sortFields(self) -> list:
        return StorageOptionManager().sortBankFields

    def sortRevert(self) -> bool:
        return StorageOptionManager().sortBankRevert
