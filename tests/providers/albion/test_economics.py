from datetime import UTC, datetime
from decimal import Decimal

import pytest

from ai_stock.analysis.arbitrage import ArbitrageOpportunity
from ai_stock.market.types import InstrumentId, MarketId
from ai_stock.providers.albion.economics import (
    AlbionMarketFeePolicy,
    calculate_net_arbitrage,
    find_profitable_net_arbitrage,
)


def _opportunity(*, buy_price: int, sell_price: int) -> ArbitrageOpportunity:
    observed_at = datetime(2026, 1, 1, tzinfo=UTC)
    gross_profit = Decimal(sell_price - buy_price)
    return ArbitrageOpportunity(
        instrument_id=InstrumentId("instrument"),
        buy_market_id=MarketId("buy-market"),
        sell_market_id=MarketId("sell-market"),
        buy_price=Decimal(buy_price),
        buy_observed_at=observed_at,
        sell_price=Decimal(sell_price),
        sell_observed_at=observed_at,
        gross_profit=gross_profit,
        gross_return_percentage=gross_profit / Decimal(buy_price) * Decimal(100),
    )


def test_calculate_net_arbitrage_applies_non_premium_sale_tax() -> None:
    result = calculate_net_arbitrage(_opportunity(buy_price=100, sell_price=125))

    assert result.sale_tax == Decimal("10.00")
    assert result.net_revenue == Decimal("115.00")
    assert result.net_profit == Decimal("15.00")
    assert result.net_return_percentage == Decimal("15.00")


def test_calculate_net_arbitrage_applies_premium_tax_reduction() -> None:
    result = calculate_net_arbitrage(
        _opportunity(buy_price=100, sell_price=125),
        AlbionMarketFeePolicy(premium=True),
    )

    assert result.sale_tax == Decimal("5.00")
    assert result.net_profit == Decimal("20.00")


def test_calculate_net_arbitrage_preserves_exact_decimal_tax() -> None:
    result = calculate_net_arbitrage(_opportunity(buy_price=100, sell_price=101))

    assert result.sale_tax == Decimal("8.08")
    assert result.net_profit == Decimal("-7.08")


def test_calculate_net_arbitrage_rejects_setup_fee_policy() -> None:
    with pytest.raises(ValueError, match="order-based execution"):
        _ = calculate_net_arbitrage(
            _opportunity(buy_price=100, sell_price=125),
            AlbionMarketFeePolicy(include_setup_fee=True),
        )


def test_find_profitable_net_arbitrage_filters_and_orders_opportunities() -> None:
    results = find_profitable_net_arbitrage(
        [
            _opportunity(buy_price=100, sell_price=101),
            _opportunity(buy_price=100, sell_price=125),
            _opportunity(buy_price=100, sell_price=150),
        ]
    )

    assert [result.net_profit for result in results] == [
        Decimal("38.00"),
        Decimal("15.00"),
    ]
