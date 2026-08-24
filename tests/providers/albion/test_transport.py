from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from ai_stock.analysis.arbitrage import ArbitrageOpportunity
from ai_stock.market.types import InstrumentId, MarketId
from ai_stock.providers.albion.economics import (
    AlbionNetArbitrageOpportunity,
    calculate_net_arbitrage,
)
from ai_stock.providers.albion.transport import (
    TransportInputs,
    calculate_transport_adjusted_opportunity,
)


def _net_opportunity() -> AlbionNetArbitrageOpportunity:
    observed_at = datetime(2026, 1, 1, tzinfo=UTC)
    return calculate_net_arbitrage(
        ArbitrageOpportunity(
            instrument_id=InstrumentId("instrument"),
            buy_market_id=MarketId("buy-market"),
            sell_market_id=MarketId("sell-market"),
            buy_price=Decimal(100),
            buy_observed_at=observed_at,
            sell_price=Decimal(125),
            sell_observed_at=observed_at,
            gross_profit=Decimal(25),
            gross_return_percentage=Decimal(25),
        )
    )


def test_calculate_transport_adjusted_opportunity() -> None:
    result = calculate_transport_adjusted_opportunity(
        _net_opportunity(),
        TransportInputs(
            quantity=25,
            transport_capacity=10,
            trip_time=timedelta(minutes=30),
        ),
    )

    assert result.units_per_trip == 10
    assert result.trip_count == 3
    assert result.total_transport_time == timedelta(minutes=90)
    assert result.full_trip_profit == Decimal("150.00")
    assert result.full_trip_profit_per_hour == Decimal("300.00")
    assert result.total_profit == Decimal("375.00")
    assert result.realization_profit_per_hour == Decimal("250.00")


@pytest.mark.parametrize(
    ("quantity", "transport_capacity", "trip_time", "message"),
    [
        (0, 1, timedelta(minutes=1), "Quantity"),
        (1, 0, timedelta(minutes=1), "Transport capacity"),
        (1, 1, timedelta(0), "Trip time"),
    ],
)
def test_transport_inputs_reject_invalid_values(
    quantity: int,
    transport_capacity: int,
    trip_time: timedelta,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        _ = TransportInputs(
            quantity=quantity,
            transport_capacity=transport_capacity,
            trip_time=trip_time,
        )
