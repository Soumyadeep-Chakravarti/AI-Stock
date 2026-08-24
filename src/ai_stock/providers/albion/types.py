from dataclasses import dataclass
from typing import NewType

AlbionItemId = NewType("AlbionItemId", str)
AlbionLocation = NewType("AlbionLocation", str)
AlbionQuality = NewType("AlbionQuality", int)


@dataclass(frozen=True, slots=True)
class AlbionCurrentPriceRecord:
    item_id: AlbionItemId
    location: AlbionLocation
    quality: AlbionQuality
    sell_price_min: int
    sell_price_min_date: str
    buy_price_max: int
    buy_price_max_date: str
