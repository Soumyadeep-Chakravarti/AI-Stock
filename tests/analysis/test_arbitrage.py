from datetime import UTC, datetime, timedelta
from decimal import Decimal

from ai_stock.analysis.arbitrage import (
    ArbitrageOpportunity,
    filter_fresh_opportunities,
    find_arbitrage_opportunities,
)
from ai_stock.market.types import CurrentPriceObservation, InstrumentId, MarketId


def _observation(
    instrument_id: str,
    market_id: str,
    bid_price: int | None,
    ask_price: int | None,
) -> CurrentPriceObservation:
    observed_at = datetime(2026, 1, 1, tzinfo=UTC)
    return CurrentPriceObservation(
        instrument_id=InstrumentId(instrument_id),
        market_id=MarketId(market_id),
        bid_price=Decimal(bid_price) if bid_price is not None else None,
        bid_observed_at=observed_at if bid_price is not None else None,
        ask_price=Decimal(ask_price) if ask_price is not None else None,
        ask_observed_at=observed_at if ask_price is not None else None,
    )


def _opportunity(
    buy_observed_at: datetime,
    sell_observed_at: datetime,
) -> ArbitrageOpportunity:
    return ArbitrageOpportunity(
        instrument_id=InstrumentId("instrument"),
        buy_market_id=MarketId("buy-market"),
        sell_market_id=MarketId("sell-market"),
        buy_price=Decimal(100),
        buy_observed_at=buy_observed_at,
        sell_price=Decimal(125),
        sell_observed_at=sell_observed_at,
        gross_profit=Decimal(25),
        gross_return_percentage=Decimal(25),
    )


def test_find_arbitrage_opportunities_returns_gross_cross_market_profit() -> None:
    opportunities = find_arbitrage_opportunities(
        [
            _observation("instrument", "buy-market", bid_price=90, ask_price=100),
            _observation("instrument", "sell-market", bid_price=125, ask_price=130),
        ]
    )

    assert len(opportunities) == 1
    opportunity = opportunities[0]
    assert opportunity.instrument_id == InstrumentId("instrument")
    assert opportunity.buy_market_id == MarketId("buy-market")
    assert opportunity.sell_market_id == MarketId("sell-market")
    assert opportunity.buy_price == Decimal(100)
    assert opportunity.buy_observed_at == datetime(2026, 1, 1, tzinfo=UTC)
    assert opportunity.sell_price == Decimal(125)
    assert opportunity.sell_observed_at == datetime(2026, 1, 1, tzinfo=UTC)
    assert opportunity.gross_profit == Decimal(25)
    assert opportunity.gross_return_percentage == Decimal(25)


def test_find_arbitrage_opportunities_ignores_invalid_or_unprofitable_quotes() -> None:
    opportunities = find_arbitrage_opportunities(
        [
            _observation("instrument", "same-market", bid_price=120, ask_price=130),
            _observation("instrument", "unprofitable", bid_price=99, ask_price=130),
            _observation("instrument", "no-ask", bid_price=90, ask_price=None),
            _observation("instrument", "no-bid", bid_price=None, ask_price=130),
        ]
    )

    assert opportunities == ()


def test_find_arbitrage_opportunities_ignores_non_positive_quotes() -> None:
    opportunities = find_arbitrage_opportunities(
        [
            _observation("instrument", "zero-ask", bid_price=None, ask_price=0),
            _observation("instrument", "negative-ask", bid_price=None, ask_price=-10),
            _observation("instrument", "zero-bid", bid_price=0, ask_price=None),
            _observation("instrument", "negative-bid", bid_price=-100, ask_price=None),
            _observation("instrument", "valid-bid", bid_price=100, ask_price=None),
        ]
    )

    assert opportunities == ()


def test_find_arbitrage_opportunities_requires_quote_timestamps() -> None:
    opportunities = find_arbitrage_opportunities(
        [
            CurrentPriceObservation(
                instrument_id=InstrumentId("instrument"),
                market_id=MarketId("buy-market"),
                bid_price=None,
                bid_observed_at=None,
                ask_price=Decimal(100),
                ask_observed_at=None,
            ),
            _observation("instrument", "sell-market", bid_price=125, ask_price=None),
        ]
    )

    assert opportunities == ()


def test_find_arbitrage_opportunities_does_not_cross_instruments() -> None:
    opportunities = find_arbitrage_opportunities(
        [
            _observation("instrument-a", "market-a", bid_price=90, ask_price=100),
            _observation("instrument-b", "market-b", bid_price=125, ask_price=130),
        ]
    )

    assert opportunities == ()


def test_find_arbitrage_opportunities_orders_by_gross_profit() -> None:
    opportunities = find_arbitrage_opportunities(
        [
            _observation("instrument", "buy-market", bid_price=90, ask_price=100),
            _observation("instrument", "smaller-profit", bid_price=120, ask_price=None),
            _observation("instrument", "larger-profit", bid_price=140, ask_price=None),
        ]
    )

    assert [opportunity.gross_profit for opportunity in opportunities] == [
        Decimal(40),
        Decimal(20),
    ]


def test_filter_fresh_opportunities_filters_quote_age_and_timestamp_skew() -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    fresh = _opportunity(
        buy_observed_at=now - timedelta(hours=1),
        sell_observed_at=now - timedelta(hours=1, minutes=15),
    )
    stale = _opportunity(
        buy_observed_at=now - timedelta(hours=3),
        sell_observed_at=now - timedelta(hours=1),
    )
    skewed = _opportunity(
        buy_observed_at=now - timedelta(hours=2),
        sell_observed_at=now - timedelta(hours=1),
    )

    opportunities = filter_fresh_opportunities(
        [fresh, stale, skewed],
        now=now,
        max_quote_age=timedelta(hours=2),
        max_timestamp_skew=timedelta(minutes=30),
    )

    assert opportunities == (fresh,)


def test_filter_fresh_opportunities_can_skip_timestamp_skew_filter() -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    skewed = _opportunity(
        buy_observed_at=now - timedelta(hours=2),
        sell_observed_at=now - timedelta(hours=1),
    )

    opportunities = filter_fresh_opportunities(
        [skewed],
        now=now,
        max_quote_age=timedelta(hours=2),
    )

    assert opportunities == (skewed,)


def test_arbitrage_opportunity_exposes_quote_age_and_timestamp_skew() -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    opportunity = _opportunity(
        buy_observed_at=now - timedelta(minutes=20),
        sell_observed_at=now - timedelta(minutes=5),
    )

    assert opportunity.buy_quote_age(now) == timedelta(minutes=20)
    assert opportunity.sell_quote_age(now) == timedelta(minutes=5)
    assert opportunity.timestamp_skew == timedelta(minutes=15)
