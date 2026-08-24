from collections.abc import Collection, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol

from ai_stock.analysis.arbitrage import (
    ArbitrageOpportunity,
    filter_fresh_opportunities,
    find_arbitrage_opportunities,
)
from ai_stock.market.types import CurrentPriceObservation, InstrumentId, MarketId
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


@dataclass(frozen=True, slots=True)
class MarketQuoteStatus:
    instrument_id: InstrumentId
    market_id: MarketId
    bid_present: bool
    ask_present: bool
    bid_age: timedelta | None
    ask_age: timedelta | None
    bid_fresh: bool
    ask_fresh: bool


@dataclass(frozen=True, slots=True)
class ArbitrageScanResult:
    opportunities: Sequence[ArbitrageOpportunity]
    quote_statuses: Sequence[MarketQuoteStatus]


def scan_arbitrage(
    client: _CurrentPriceClient,
    *,
    item_ids: Collection[AlbionItemId],
    locations: Collection[AlbionLocation],
    qualities: Collection[AlbionQuality],
    now: datetime,
    max_quote_age: timedelta,
    max_timestamp_skew: timedelta | None = None,
) -> ArbitrageScanResult:
    observations = client.get_current_prices(item_ids, locations, qualities)
    opportunities = find_arbitrage_opportunities(observations)
    return ArbitrageScanResult(
        opportunities=filter_fresh_opportunities(
            opportunities,
            now=now,
            max_quote_age=max_quote_age,
            max_timestamp_skew=max_timestamp_skew,
        ),
        quote_statuses=tuple(
            _quote_status(observation, now, max_quote_age)
            for observation in observations
        ),
    )


def _quote_status(
    observation: CurrentPriceObservation,
    now: datetime,
    max_quote_age: timedelta,
) -> MarketQuoteStatus:
    bid_age = (
        now - observation.bid_observed_at
        if observation.bid_observed_at is not None
        else None
    )
    ask_age = (
        now - observation.ask_observed_at
        if observation.ask_observed_at is not None
        else None
    )
    return MarketQuoteStatus(
        instrument_id=observation.instrument_id,
        market_id=observation.market_id,
        bid_present=observation.bid_price is not None,
        ask_present=observation.ask_price is not None,
        bid_age=bid_age,
        ask_age=ask_age,
        bid_fresh=bid_age is not None and bid_age <= max_quote_age,
        ask_fresh=ask_age is not None and ask_age <= max_quote_age,
    )
