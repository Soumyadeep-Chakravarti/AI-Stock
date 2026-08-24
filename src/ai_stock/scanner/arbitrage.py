from collections.abc import Collection, Sequence
from datetime import datetime, timedelta
from typing import Protocol

from ai_stock.analysis.arbitrage import (
    ArbitrageOpportunity,
    filter_fresh_opportunities,
    find_arbitrage_opportunities,
)
from ai_stock.market.types import CurrentPriceObservation
from ai_stock.providers.albion.types import (
    AlbionItemId,
    AlbionLocation,
    AlbionQuality,
)


class _CurrentPriceClient(Protocol):
    def get_current_prices(
        self,
        item_ids: Collection[AlbionItemId],
        locations: Collection[AlbionLocation],
        qualities: Collection[AlbionQuality] = (),
    ) -> Sequence[CurrentPriceObservation]: ...


def scan_arbitrage(
    client: _CurrentPriceClient,
    *,
    item_ids: Collection[AlbionItemId],
    locations: Collection[AlbionLocation],
    qualities: Collection[AlbionQuality],
    now: datetime,
    max_quote_age: timedelta,
    max_timestamp_skew: timedelta | None = None,
) -> Sequence[ArbitrageOpportunity]:
    observations = client.get_current_prices(item_ids, locations, qualities)
    opportunities = find_arbitrage_opportunities(observations)
    return filter_fresh_opportunities(
        opportunities,
        now=now,
        max_quote_age=max_quote_age,
        max_timestamp_skew=max_timestamp_skew,
    )
