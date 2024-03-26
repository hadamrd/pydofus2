from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeCraftResultWithObjectDescMessage import \
    ExchangeCraftResultWithObjectDescMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemNotInContainer import \
        ObjectItemNotInContainer


class ExchangeCraftResultMagicWithObjectDescMessage(ExchangeCraftResultWithObjectDescMessage):
    magicPoolStatus: int

    def init(self, magicPoolStatus_: int, objectInfo_: "ObjectItemNotInContainer", craftResult_: int):
        self.magicPoolStatus = magicPoolStatus_

        super().init(objectInfo_, craftResult_)
