from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.StorageOptionManager import StorageOptionManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.inventoryView.StorageGenericView import StorageGenericView
from pydofus2.com.ankamagames.dofus.types.enums.ItemCategoryEnum import ItemCategoryEnum


class BankRessourcesView(StorageGenericView):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "bankRessources"

    def isListening(self, item: ItemWrapper) -> bool:
        return (
            super().isListening(item)
            and item.category == ItemCategoryEnum.RESOURCES_CATEGORY
            and item.typeId != DataEnum.ITEM_TYPE_ECAFLIP_CARD
        )

    def updateView(self) -> None:
        super().updateView()

    def sortFields(self) -> list:
        return StorageOptionManager().sortBankFields

    def sortRevert(self) -> bool:
        return StorageOptionManager().sortBankRevert
