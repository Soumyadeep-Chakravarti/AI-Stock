from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from ai_stock.analysis.statistics import (
    absolute_price_change,
    mean_price,
    percentage_price_change,
    population_price_volatility,
    sample_price_volatility,
)
from ai_stock.market.types import HistoricalPriceObservation, InstrumentId, MarketId


def _observation(price: int, hour: int) -> HistoricalPriceObservation:
    return HistoricalPriceObservation(
        instrument_id=InstrumentId("instrument"),
        market_id=MarketId("market"),
        price=Decimal(price),
        observed_at=datetime(2026, 1, 1, tzinfo=UTC) + timedelta(hours=hour),
    )


def test_mean_price() -> None:
    observations = [_observation(10, 0), _observation(20, 1), _observation(40, 2)]

    assert mean_price(observations) == Decimal(70) / 3


def test_price_changes_use_chronological_order() -> None:
    observations = [_observation(20, 1), _observation(10, 0), _observation(40, 2)]

    assert absolute_price_change(observations) == Decimal(30)
    assert percentage_price_change(observations) == Decimal(300)


def test_population_price_volatility() -> None:
    observations = [_observation(1, 0), _observation(2, 1), _observation(3, 2)]

    assert population_price_volatility(observations).quantize(
        Decimal("0.000001")
    ) == Decimal("0.816497")


def test_sample_price_volatility() -> None:
    observations = [_observation(1, 0), _observation(2, 1), _observation(3, 2)]

    assert sample_price_volatility(observations) == Decimal(1)


def test_statistics_reject_empty_series() -> None:
    with pytest.raises(ValueError, match="At least one observation"):
        _ = mean_price([])


def test_percentage_price_change_rejects_zero_start_price() -> None:
    observations = [_observation(0, 0), _observation(10, 1)]

    with pytest.raises(ValueError, match="zero price"):
        _ = percentage_price_change(observations)


def test_sample_price_volatility_requires_two_observations() -> None:
    with pytest.raises(ValueError, match="at least two observations"):
        _ = sample_price_volatility([_observation(10, 0)])
