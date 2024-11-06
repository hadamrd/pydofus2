from typing import TYPE_CHECKING, List, Optional

from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.managers.MarketBidsManager import MarketBidsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InactivityManager import InactivityManager
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.npc.NpcGenericActionRequestMessage import (
    NpcGenericActionRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHouseInListUpdatedMessage import (
    ExchangeBidHouseInListUpdatedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHouseItemAddOkMessage import (
    ExchangeBidHouseItemAddOkMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHouseItemRemoveOkMessage import (
    ExchangeBidHouseItemRemoveOkMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHousePriceMessage import (
    ExchangeBidHousePriceMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHouseSearchMessage import (
    ExchangeBidHouseSearchMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidPriceForSellerMessage import (
    ExchangeBidPriceForSellerMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectModifyPricedMessage import (
    ExchangeObjectModifyPricedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeObjectMovePricedMessage import (
    ExchangeObjectMovePricedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedBidBuyerMessage import (
    ExchangeStartedBidBuyerMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedBidSellerMessage import (
    ExchangeStartedBidSellerMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeTypesItemsExchangerDescriptionForUserMessage import (
    ExchangeTypesItemsExchangerDescriptionForUserMessage,
)
from pydofus2.com.ankamagames.dofus.types.enums.ItemCategoryEnum import ItemCategoryEnum
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.common.managers.MarketBid import MarketBid


class MarketFrame(Frame):
    """
    Frame for handling marketplace operations and state management.
    Processes market-related messages and maintains market state.
    """

    # Marketplace constants
    SELL_MODE_ACTION_ID = 5
    BUY_MODE_ACTION_ID = 6
    RESOURCE_MARKETPLACE_ELEMENT_TYPE_ID = 313
    RESOURCES_MARKETPLACE_GFX_ID = 226

    # Market type mapping
    ITEM_TYPE_TO_MARKETPLACE_GFX_ID = {
        ItemCategoryEnum.RESOURCES_CATEGORY: RESOURCES_MARKETPLACE_GFX_ID,
    }

    def __init__(self):
        """Initialize market frame"""
        super().__init__()
        self._logger = Logger()
        self._bids_manager = MarketBidsManager()
        self._current_searched_item_gid: Optional[ItemWrapper] = None
        self._market_type_open = None
        self._state = "INIT"
        self._current_mode = None
        self._market_mapId = None

    @property
    def priority(self) -> int:
        """Frame priority for message processing"""
        return Priority.NORMAL

    def pushed(self) -> bool:
        """Called when frame is pushed to stack"""
        self._bids_manager = MarketBidsManager()
        self._market_type_open = None
        self._state = "INIT"
        return True

    def reset_state(self):
        self._market_type_open = None
        self._current_mode = None
        self._current_searched_item_gid = None

    def pulled(self) -> bool:
        """Called when frame is pulled from stack"""
        self.reset_state()
        return True

    def process(self, msg: Message) -> bool:
        """
        Process incoming market-related messages
        Args:
            msg: Message to process
        Returns: True if message was handled
        """
        # Handle sell mode initialization
        if isinstance(msg, ExchangeStartedBidSellerMessage):
            if self._state != "SWITCHING_TO_SELL":
                KernelEventsManager().send(
                    KernelEvent.ClientShutdown,
                    "Received 'ExchangeStartedBidSellerMessage' but wasn't expecting market mode switch!",
                )
                return

            Logger().info("Market switched to sell mode")
            self._state = "IDLE"
            self._logger.info("Initialize market state with rules from seller descriptor")
            self._bids_manager.init_from_seller_descriptor(msg)
            KernelEventsManager().send(KernelEvent.MarketModeSwitch, "sell")
            return True

        elif isinstance(msg, ExchangeStartedBidBuyerMessage):
            return True

        # Handle item type descriptions
        if isinstance(msg, ExchangeTypesItemsExchangerDescriptionForUserMessage):
            if self._state != "SEARCHING":
                KernelEventsManager().send(
                    KernelEvent.ClientShutdown,
                    "Received 'ExchangeTypesItemsExchangerDescriptionForUserMessage' but wasn't searching any item!",
                )
                return

            self._logger.debug(f"Received item research result for GID {msg.objectGID}")
            self._state = "IDLE"
            self._current_searched_item_gid = self._bids_manager.handle_search_result(msg)
            KernelEventsManager().send(KernelEvent.MarketSearchResult, msg)
            return True

        # Price check response
        if isinstance(msg, ExchangeBidPriceForSellerMessage):
            if self._state != "CHECKING_PRICE":
                KernelEventsManager().send(
                    KernelEvent.ClientShutdown,
                    "Received 'ExchangeBidPriceForSellerMessage' but wasn't checking any item price!",
                )
                return

            self._state = "IDLE"
            self._bids_manager.handle_price_info(msg)
            self._current_mode = "sell"
            KernelEventsManager().send(KernelEvent.MarketPriceInfo, msg)
            return True

        # Real-time price updates
        if isinstance(msg, ExchangeBidHouseInListUpdatedMessage):
            changes = self._bids_manager.handle_market_update(msg)
            if changes:
                for gid, quantity, old_price, new_price in changes:
                    KernelEventsManager().send(KernelEvent.MarketPriceChanged, gid, quantity, old_price, new_price)
            return True

        # New listing added
        if isinstance(msg, ExchangeBidHouseItemAddOkMessage):
            listing = self._bids_manager.handle_bid_added(msg)
            if listing:
                self._logger.info(f"Added listing {listing.uid} to market state")
                KernelEventsManager().send(KernelEvent.MarketListingAdded, listing)
            return True

        # Listing removed/sold
        if isinstance(msg, ExchangeBidHouseItemRemoveOkMessage):
            listing = self._bids_manager.handle_bid_removed(msg)
            if listing:
                self._logger.info(f"Removed listing {listing.uid} from market state")
                KernelEventsManager().send(KernelEvent.MarketListingRemoved, listing)
            return True

    # Market Operations
    def search_item(self, item_gid: int, callback=None) -> None:
        self._state = "SEARCHING"
        if callback:
            KernelEventsManager().once(KernelEvent.MarketSearchResult, callback)
        msg = ExchangeBidHouseSearchMessage()
        msg.init(item_gid, True)  # Enable following
        ConnectionsHandler().send(msg)
        InactivityManager().activity()

    def check_price(self, item_gid: int, callback=None) -> None:
        self._state = "CHECKING_PRICE"
        if callback:
            KernelEventsManager().once(KernelEvent.MarketPriceInfo, callback, originator=self)
        Logger().info(f"Sending check price for item {item_gid}")
        msg = ExchangeBidHousePriceMessage()
        msg.init(item_gid)
        ConnectionsHandler().send(msg)
        InactivityManager().activity()

    def create_listing(self, item_uid: int, quantity: int, price: int) -> None:
        self._state = "SELLING"
        msg = ExchangeObjectMovePricedMessage()
        msg.init(price, item_uid, quantity)
        ConnectionsHandler().send(msg)
        InactivityManager().activity()

    def send_update_listing(self, listing_uid: int, quantity: int, new_price: int) -> None:
        self._state = "UPDATING"
        msg = ExchangeObjectModifyPricedMessage()
        msg.init(new_price, listing_uid, quantity)
        ConnectionsHandler().send(msg)
        InactivityManager().activity()

    def switch_mode(self, mode, callback=None) -> bool:
        """Start the mode switch sequence"""
        self._logger.debug(f"Switching to {mode} mode ...")
        self._state = "SWITCHING_TO_SELL"
        action_id = self.SELL_MODE_ACTION_ID if mode == "sell" else self.BUY_MODE_ACTION_ID
        if callback:
            KernelEventsManager().once(KernelEvent.MarketModeSwitch, callback, originator=self)
        msg = NpcGenericActionRequestMessage()
        msg.init(-1, action_id, self._market_mapId)
        ConnectionsHandler().send(msg)
        InactivityManager().activity()

    def get_listings(self, item_gid: int, quantity: int) -> List["MarketBid"]:
        """Get current listings for item and quantity"""
        return self._bids_manager.get_bids(item_gid, quantity)

    def get_best_price(self, item_gid: int, quantity: int) -> Optional[int]:
        """Get current best price for item and quantity"""
        return self._bids_manager.min_price[item_gid][quantity]

    def get_average_price(self, item_gid: int, quantity: int) -> Optional[int]:
        """Get average price for item and quantity"""
        return self._bids_manager.avg_prices[item_gid][quantity]

    def calculate_tax(self, price: int) -> int:
        """Calculate listing tax amount"""
        return self._bids_manager.calculate_tax(price)
