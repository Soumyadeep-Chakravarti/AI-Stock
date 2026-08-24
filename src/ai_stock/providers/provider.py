from collections.abc import Collection, Sequence
from datetime import datetime, timedelta
from typing import Protocol

from ai_stock.market.types import (
    CurrentPriceObservation,
    HistoricalPriceObservation,
    InstrumentId,
    MarketId,
)


class MarketDataProvider(Protocol):
    def get_current_prices(
        self,
        instrument_ids: Collection[InstrumentId],
        market_ids: Collection[MarketId],
    ) -> Sequence[CurrentPriceObservation]: ...

    def get_historical_prices(
        self,
        instrument_id: InstrumentId,
        market_id: MarketId,
        start: datetime | None = None,
        end: datetime | None = None,
        interval: timedelta | None = None,
    ) -> Sequence[HistoricalPriceObservation]: ...
