from collections.abc import Sequence
from dataclasses import dataclass
from enum import IntEnum
from typing import NewType

AlbionItemId = NewType("AlbionItemId", str)
AlbionLocation = NewType("AlbionLocation", str)
AlbionQuality = NewType("AlbionQuality", int)


class AlbionHistoryInterval(IntEnum):
    HOUR = 1
    SIX_HOURS = 6
    DAY = 24


@dataclass(frozen=True, slots=True)
class AlbionCurrentPriceRecord:
    item_id: AlbionItemId
    location: AlbionLocation
    quality: AlbionQuality
    sell_price_min: int
    sell_price_min_date: str
    buy_price_max: int
    buy_price_max_date: str


@dataclass(frozen=True, slots=True)
class AlbionHistoricalPricePoint:
    """A sell-order bucket whose item count is not confirmed trade volume."""

    item_count: int
    avg_price: int
    timestamp: str


@dataclass(frozen=True, slots=True)
class AlbionHistoricalPriceRecord:
    item_id: AlbionItemId
    location: AlbionLocation
    quality: AlbionQuality
    data: Sequence[AlbionHistoricalPricePoint]
