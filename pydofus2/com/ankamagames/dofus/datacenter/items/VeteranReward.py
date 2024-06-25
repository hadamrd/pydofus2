from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class VeteranReward(IDataCenter):

    MODULE: str = "VeteranRewards"

    id: int

    requiredSubDays: int

    itemGID: int

    itemQuantity: int

    _itemWrapper: ItemWrapper = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getAllVeteranRewards(cls) -> list:
        return GameData().getObjects(cls.MODULE)

    @property
    def item(self) -> ItemWrapper:
        if not self._itemWrapper:
            self._itemWrapper = ItemWrapper.create(0, 0, self.itemGID, self.itemQuantity, None, False)
        return self._itemWrapper
