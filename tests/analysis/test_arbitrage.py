from datetime import UTC, datetime
from decimal import Decimal

from ai_stock.analysis.arbitrage import find_arbitrage_opportunities
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
    assert opportunity.sell_price == Decimal(125)
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
