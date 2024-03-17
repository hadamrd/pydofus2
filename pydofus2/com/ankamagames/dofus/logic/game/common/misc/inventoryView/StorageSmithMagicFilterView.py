from pydofus2.com.ankamagames.dofus.datacenter.jobs.Skill import Skill
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.inventoryView.StorageGenericView import \
    StorageGenericView
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.IStorageView import \
    IStorageView


class StorageSmithMagicFilterView(StorageGenericView):

    _skill: Skill

    _parent: IStorageView

    _listeningItemTypes: list

    def __init__(self, parentView: IStorageView, skill: Skill):
        self._listeningItemTypes = [
            DataEnum.ITEM_TYPE_SMITHMAGIC_RUNE,
            DataEnum.ITEM_TYPE_SMITHMAGIC_POTION,
            DataEnum.ITEM_TYPE_SMITHMAGIC_ORB,
            DataEnum.ITEM_TYPE_SMITHMAGIC_TRANSCENDANCE_RUNE,
            DataEnum.ITEM_TYPE_SMITHMAGIC_CORRUPTION_RUNE,
        ]
        super().__init__()
        self._skill = skill
        self._parent = parentView

    @property
    def name(self) -> str:
        return "storageSmithMagicFilter"

    def isListening(self, item: ItemWrapper) -> bool:
        return (
            self._parent.isListening(item)
            and super().isListening(item)
            and (item.typeId in self._skill.modifiableItemTypeIds or item.typeId in self._listeningItemTypes)
            or item.objectGID == DataEnum.ITEM_GID_SIGNATURE_RUNE
        )

    def updateView(self) -> None:
        super().updateView()

    @property
    def parent(self) -> IStorageView:
        return self._parent

    @parent.setter
    def parent(self, view: IStorageView) -> None:
        self._parent = view
