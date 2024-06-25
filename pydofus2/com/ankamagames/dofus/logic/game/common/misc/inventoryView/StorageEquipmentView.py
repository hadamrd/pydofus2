from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.inventoryView.StorageGenericView import StorageGenericView
from pydofus2.com.ankamagames.dofus.types.enums.ItemCategoryEnum import ItemCategoryEnum


class StorageEquipmentView(StorageGenericView):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "storageEquipment"

    def isListening(self, item: ItemWrapper) -> bool:
        return super().isListening(item) and item.category == ItemCategoryEnum.EQUIPMENT_CATEGORY

    def updateView(self) -> None:
        super().updateView()
