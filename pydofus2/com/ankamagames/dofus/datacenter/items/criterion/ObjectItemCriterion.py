from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import \
    ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import \
    InventoryManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import \
    PatternDecoder


class ObjectItemCriterion(ItemCriterion, IDataCenter):


    def __init__(self, pCriterion: str):
        self._criterionValueQuantity = -1
        super().__init__(pCriterion)
        if self._criterionValue == 0 and "," in self._criterionValueText:
            itemIdAndQuantity = self._criterionValueText.split(",")
            self._criterionValue = int(itemIdAndQuantity[0])
            self._criterionValueQuantity = int(itemIdAndQuantity[1])
            if self._criterionValueQuantity == 0 and str(itemIdAndQuantity[1]).index("0") == -1:
                self._criterionValueQuantity = -1

    @property
    def isRespected(self) -> bool:
        iw: ItemWrapper = None
        itemQuantity: int = 0
        for iw in InventoryManager().realInventory:
            if iw.objectGID == self._criterionValue:
                itemQuantity = iw.quantity
                break
        if self._operator.text == ItemCriterionOperator.EQUAL:
            return (
                self._criterionValueQuantity == itemQuantity > 0
                if -1
                else itemQuantity == self._criterionValueQuantity
            )
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            return (
                self._criterionValueQuantity == itemQuantity == 0
                if -1
                else itemQuantity != self._criterionValueQuantity
            )
        if self._operator.text == ItemCriterionOperator.SUPERIOR:
            return itemQuantity > max(self._criterionValueQuantity, 0)
        if self._operator.text == ItemCriterionOperator.INFERIOR:
            return itemQuantity < max(self._criterionValueQuantity, 1)
        return False

    @property
    def text(self) -> str:
        objectItem = Item.getItemById(self._criterionValue)
        if objectItem.type.superTypeId == DataEnum.ITEM_SUPERTYPE_INVISIBLE:
            return ""
        objectName = objectItem.name
        readableCriterion = ""
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            if self._criterionValueQuantity == 1 or self._criterionValueQuantity == -1:
                readableCriterion = I18n.getUiText("ui.common.doNotPossess", [objectName])
            else:
                readableCriterion = I18n.getUiText(
                    "ui.common.doNotPossessQuantity", [self._criterionValueQuantity, objectName]
                )

        elif self._operator.text == ItemCriterionOperator.EQUAL:
            if self._criterionValueQuantity == 1 or self._criterionValueQuantity == -1:
                readableCriterion = I18n.getUiText("ui.common.doPossess", [objectName])
            else:
                readableCriterion = I18n.getUiText(
                    "ui.common.doPossessQuantity", [self._criterionValueQuantity, objectName]
                )

        elif self._operator.text == ItemCriterionOperator.SUPERIOR:
            if self._criterionValueQuantity == 0:
                readableCriterion = I18n.getUiText("ui.common.doPossess", [objectName])
            else:
                readableCriterion = PatternDecoder.combine(I18n.getUiText(
                    "ui.common.doPossessQuantityOrMore", [self._criterionValueQuantity + 1, objectName]
                ))

        elif self._operator.text == ItemCriterionOperator.INFERIOR:
            if self._criterionValueQuantity == 1:
                readableCriterion = I18n.getUiText("ui.common.doNotPossess", [objectName])
            else:
                readableCriterion = PatternDecoder.combine(I18n.getUiText(
                    "ui.common.doPossessQuantityOrLess", [self._criterionValueQuantity - 1, objectName]
                ))

        elif self._operator.text == ItemCriterionOperator.EQUIPPED:
            readableCriterion = I18n.getUiText("ui.common.doEquip",[objectName])
            
        elif self._operator.text == ItemCriterionOperator.NOT_EQUIPPED:
            readableCriterion = I18n.getUiText("ui.common.doNotEquip",[objectName])

        return readableCriterion

    def clone(self) -> IItemCriterion:
        return ObjectItemCriterion(self.basicText)
