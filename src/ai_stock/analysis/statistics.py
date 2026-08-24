from collections.abc import Sequence
from decimal import Decimal

from ai_stock.market.types import HistoricalPriceObservation


def mean_price(observations: Sequence[HistoricalPriceObservation]) -> Decimal:
    prices = _prices(observations)
    return sum(prices, Decimal(0)) / Decimal(len(prices))


def absolute_price_change(
    observations: Sequence[HistoricalPriceObservation],
) -> Decimal:
    prices = _chronological_prices(observations)
    return prices[-1] - prices[0]


def percentage_price_change(
    observations: Sequence[HistoricalPriceObservation],
) -> Decimal:
    prices = _chronological_prices(observations)
    if prices[0] == 0:
        raise ValueError("Cannot calculate percentage change from a zero price")
    return (prices[-1] - prices[0]) / prices[0] * Decimal(100)


def population_price_volatility(
    observations: Sequence[HistoricalPriceObservation],
) -> Decimal:
    prices = _prices(observations)
    mean = sum(prices, Decimal(0)) / Decimal(len(prices))
    variance = sum(
        ((price - mean) ** 2 for price in prices),
        Decimal(0),
    ) / Decimal(len(prices))
    return variance.sqrt()


def sample_price_volatility(
    observations: Sequence[HistoricalPriceObservation],
) -> Decimal:
    prices = _prices(observations)
    if len(prices) < 2:
        raise ValueError("Sample volatility requires at least two observations")
    mean = sum(prices, Decimal(0)) / Decimal(len(prices))
    variance = sum(
        ((price - mean) ** 2 for price in prices),
        Decimal(0),
    ) / Decimal(len(prices) - 1)
    return variance.sqrt()


def _prices(observations: Sequence[HistoricalPriceObservation]) -> tuple[Decimal, ...]:
    if not observations:
        raise ValueError("At least one observation is required")
    return tuple(observation.price for observation in observations)


def _chronological_prices(
    observations: Sequence[HistoricalPriceObservation],
) -> tuple[Decimal, ...]:
    if not observations:
        raise ValueError("At least one observation is required")
    return tuple(
        observation.price
        for observation in sorted(
            observations, key=lambda observation: observation.observed_at
        )
    )
