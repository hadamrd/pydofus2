from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.inventoryView.StorageGenericView import StorageGenericView
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.IStorageView import IStorageView


class StorageBidHouseFilterView(StorageGenericView):

    _allowedTypes: list[int]

    _maxItemLevel: int

    _parent: IStorageView

    def __init__(
        self,
        parentView: IStorageView,
        allowedTypes: list[int],
        maxItemLevel: int,
    ):
        super().__init__()
        self._allowedTypes = allowedTypes
        self._maxItemLevel = maxItemLevel
        self._parent = parentView

    @property
    def name(self) -> str:
        return "storageBidHouseFilter"

    def isListening(self, item: ItemWrapper) -> bool:
        data: Item = Item.getItemById(item.objectGID)
        return (
            self._parent.isListening(item)
            and super().isListening(item)
            and data.level <= self._maxItemLevel
            and data.typeId in self._allowedTypes
        )

    def updateView(self) -> None:
        super().updateView()

    @property
    def parent(self) -> IStorageView:
        return self._parent

    @parent.setter
    def parent(self, view: IStorageView) -> None:
        self._parent = view
