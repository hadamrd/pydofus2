from dataclasses import dataclass
from typing import Optional

from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemToSellInBid import ObjectItemToSellInBid


@dataclass
class MarketBid:
    """Represents one of our market listings with tracking data"""

    uid: int
    price: int
    quantity: int
    unsold_delay: int
    max_delay: int
    item_type: Optional[int] = None
    item_gid: Optional[int] = None

    @property
    def age(self) -> int:
        return max(0, self.max_delay - self.unsold_delay)

    @property
    def age_hours(self) -> float:
        return self.age / 3600

    @property
    def time_left(self) -> int:
        """Time remaining on the listing in seconds"""
        return max(0, self.unsold_delay)

    @property
    def formatted_time_left(self) -> str:
        """Time remaining formatted as 'Xd HH:MM' or 'HH:MM'"""
        seconds = self.time_left
        days = seconds // (24 * 3600)
        remaining = seconds % (24 * 3600)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60

        if days > 0:
            return f"{days}d {hours:02d}:{minutes:02d}"
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}"
        return f"{minutes:02d}"

    def __lt__(self, other: "MarketBid"):
        """Sort by highest price first, then oldest first"""
        if self.price != other.price:
            return self.price > other.price  # Higher price first
        return self.unsold_delay > other.unsold_delay  # Lower delay = older listing

    @classmethod
    def from_message(cls, info: "ObjectItemToSellInBid", max_delay: int) -> "MarketBid":
        return cls(
            uid=info.objectUID,
            price=info.objectPrice,
            quantity=info.quantity,
            unsold_delay=info.unsoldDelay,
            max_delay=max_delay,
            item_type=info.effects.typeId if hasattr(info, "effects") and info.effects else None,
            item_gid=info.objectGID,
        )
