from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHouseInListAddedMessage import (
    ExchangeBidHouseInListAddedMessage,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import ObjectEffect


class ExchangeBidHouseInListUpdatedMessage(ExchangeBidHouseInListAddedMessage):
    def init(
        self, itemUID_: int, objectGID_: int, objectType_: int, effects_: list["ObjectEffect"], prices_: list[int]
    ):

        super().init(itemUID_, objectGID_, objectType_, effects_, prices_)
