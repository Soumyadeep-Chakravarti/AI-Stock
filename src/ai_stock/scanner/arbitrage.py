from collections.abc import Collection, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
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
class ScanCoverage:
    instrument_id: InstrumentId
    requested_market_count: int
    returned_record_count: int
    fresh_bid_count: int
    fresh_ask_count: int
    usable_market_count: int
    usable_market_ratio: Decimal


@dataclass(frozen=True, slots=True)
class ArbitrageScanResult:
    opportunities: Sequence[ArbitrageOpportunity]
    quote_statuses: Sequence[MarketQuoteStatus]
    coverage: Sequence[ScanCoverage]


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
        coverage=_coverage(item_ids, locations, observations, now, max_quote_age),
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


def _coverage(
    item_ids: Collection[AlbionItemId],
    locations: Collection[AlbionLocation],
    observations: Sequence[CurrentPriceObservation],
    now: datetime,
    max_quote_age: timedelta,
) -> Sequence[ScanCoverage]:
    requested_market_count = len(locations)
    coverage: list[ScanCoverage] = []

    for item_id in item_ids:
        instrument_id = InstrumentId(item_id)
        statuses = tuple(
            _quote_status(observation, now, max_quote_age)
            for observation in observations
            if observation.instrument_id == instrument_id
        )
        usable_market_count = sum(
            status.bid_fresh and status.ask_fresh for status in statuses
        )
        coverage.append(
            ScanCoverage(
                instrument_id=instrument_id,
                requested_market_count=requested_market_count,
                returned_record_count=len(statuses),
                fresh_bid_count=sum(status.bid_fresh for status in statuses),
                fresh_ask_count=sum(status.ask_fresh for status in statuses),
                usable_market_count=usable_market_count,
                usable_market_ratio=(
                    Decimal(usable_market_count) / Decimal(requested_market_count)
                    if requested_market_count > 0
                    else Decimal(0)
                ),
            )
        )

    return tuple(coverage)
