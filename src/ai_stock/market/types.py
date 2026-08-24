from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import NewType

InstrumentId = NewType("InstrumentId", str)
MarketId = NewType("MarketId", str)


@dataclass(frozen=True, slots=True)
class CurrentPriceObservation:
    instrument_id: InstrumentId
    market_id: MarketId
    bid_price: Decimal | None
    bid_observed_at: datetime | None
    ask_price: Decimal | None
    ask_observed_at: datetime | None


@dataclass(frozen=True, slots=True)
class HistoricalPriceObservation:
    instrument_id: InstrumentId
    market_id: MarketId
    price: Decimal
    observed_at: datetime
    quantity: Decimal | None = None
