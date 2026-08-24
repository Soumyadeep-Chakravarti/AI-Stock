from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from ai_stock.market.types import CurrentPriceObservation, InstrumentId, MarketId


@dataclass(frozen=True, slots=True)
class ArbitrageOpportunity:
    """A gross cross-market opportunity before costs and freshness checks."""

    instrument_id: InstrumentId
    buy_market_id: MarketId
    sell_market_id: MarketId
    buy_price: Decimal
    buy_observed_at: datetime
    sell_price: Decimal
    sell_observed_at: datetime
    gross_profit: Decimal
    gross_return_percentage: Decimal

    def buy_quote_age(self, now: datetime) -> timedelta:
        return now - self.buy_observed_at

    def sell_quote_age(self, now: datetime) -> timedelta:
        return now - self.sell_observed_at

    @property
    def timestamp_skew(self) -> timedelta:
        return abs(self.buy_observed_at - self.sell_observed_at)


def find_arbitrage_opportunities(
    observations: Sequence[CurrentPriceObservation],
) -> Sequence[ArbitrageOpportunity]:
    opportunities: list[ArbitrageOpportunity] = []

    for buy_observation in observations:
        if (
            buy_observation.ask_price is None
            or buy_observation.ask_price <= 0
            or buy_observation.ask_observed_at is None
        ):
            continue

        for sell_observation in observations:
            if (
                sell_observation.instrument_id != buy_observation.instrument_id
                or sell_observation.market_id == buy_observation.market_id
                or sell_observation.bid_price is None
                or sell_observation.bid_price <= 0
                or sell_observation.bid_observed_at is None
            ):
                continue

            gross_profit = sell_observation.bid_price - buy_observation.ask_price
            if gross_profit <= 0:
                continue

            opportunities.append(
                ArbitrageOpportunity(
                    instrument_id=buy_observation.instrument_id,
                    buy_market_id=buy_observation.market_id,
                    sell_market_id=sell_observation.market_id,
                    buy_price=buy_observation.ask_price,
                    buy_observed_at=buy_observation.ask_observed_at,
                    sell_price=sell_observation.bid_price,
                    sell_observed_at=sell_observation.bid_observed_at,
                    gross_profit=gross_profit,
                    gross_return_percentage=(
                        gross_profit / buy_observation.ask_price * Decimal(100)
                    ),
                )
            )

    return tuple(
        sorted(
            opportunities,
            key=lambda opportunity: opportunity.gross_profit,
            reverse=True,
        )
    )


def filter_fresh_opportunities(
    opportunities: Sequence[ArbitrageOpportunity],
    *,
    now: datetime,
    max_quote_age: timedelta,
    max_timestamp_skew: timedelta | None = None,
) -> Sequence[ArbitrageOpportunity]:
    """Return opportunities whose quote ages and optional timestamp skew are acceptable."""
    return tuple(
        opportunity
        for opportunity in opportunities
        if opportunity.buy_quote_age(now) <= max_quote_age
        and opportunity.sell_quote_age(now) <= max_quote_age
        and (
            max_timestamp_skew is None
            or opportunity.timestamp_skew <= max_timestamp_skew
        )
    )
