from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper


class HyperlinkItemManager:
    _itemId = 0
    _itemList = {}
    lastItemTooltipId = -1

    @staticmethod
    def getItemName(objectGID: int, objectUID: int = 0) -> str:
        item = Item.getItemById(objectGID)
        if item:
            return "[" + item.name + "]"
        return "[null]"

    @staticmethod
    def newChatItem(item: ItemWrapper) -> str:
        HyperlinkItemManager._itemList[HyperlinkItemManager._itemId] = item
        code = "{chatitem," + str(HyperlinkItemManager._itemId) + "::[" + item.realName + "]}"
        HyperlinkItemManager._itemId += 1
        return code
