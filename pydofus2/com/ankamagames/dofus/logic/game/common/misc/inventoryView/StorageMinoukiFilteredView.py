from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.StorageOptionManager import StorageOptionManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.inventoryView.StorageMinoukiView import StorageMinoukiView


class StorageMinoukiFilteredView(StorageMinoukiView):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "storageMinoukiFiltered"

    def isListening(self, item: ItemWrapper) -> bool:
        return (
            super().isListening(item)
            and StorageOptionManager().hasFilter()
            and self.hasMinoukiEffect(item, StorageOptionManager().filter)
        )

    def hasMinoukiEffect(self, item: ItemWrapper, filter: int) -> bool:
        for effect in item.possibleEffects:
            if effect.effectId == ActionIds.ACTION_ITEM_CUSTOM_EFFECT:
                if effect.parameter2 == filter:
                    return True
        return False
