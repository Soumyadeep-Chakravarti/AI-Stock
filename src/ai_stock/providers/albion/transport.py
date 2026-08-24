from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

from ai_stock.providers.albion.economics import AlbionNetArbitrageOpportunity


@dataclass(frozen=True, slots=True)
class TransportInputs:
    """Caller-measured inputs for one complete transport cycle."""

    quantity: int
    transport_capacity: int
    trip_time: timedelta

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if self.transport_capacity <= 0:
            raise ValueError("Transport capacity must be greater than zero")
        if self.trip_time <= timedelta(0):
            raise ValueError("Trip time must be greater than zero")


@dataclass(frozen=True, slots=True)
class TransportAdjustedOpportunity:
    net_opportunity: AlbionNetArbitrageOpportunity
    requested_quantity: int
    units_per_trip: int
    trip_count: int
    trip_time: timedelta
    profit_per_trip: Decimal
    total_profit: Decimal
    profit_per_hour: Decimal


def calculate_transport_adjusted_opportunity(
    net_opportunity: AlbionNetArbitrageOpportunity,
    inputs: TransportInputs,
) -> TransportAdjustedOpportunity:
    units_per_trip = min(inputs.quantity, inputs.transport_capacity)
    trip_count = (
        inputs.quantity + inputs.transport_capacity - 1
    ) // inputs.transport_capacity
    profit_per_trip = net_opportunity.net_profit * Decimal(units_per_trip)
    total_profit = net_opportunity.net_profit * Decimal(inputs.quantity)
    profit_per_hour = profit_per_trip / _duration_hours(inputs.trip_time)

    return TransportAdjustedOpportunity(
        net_opportunity=net_opportunity,
        requested_quantity=inputs.quantity,
        units_per_trip=units_per_trip,
        trip_count=trip_count,
        trip_time=inputs.trip_time,
        profit_per_trip=profit_per_trip,
        total_profit=total_profit,
        profit_per_hour=profit_per_hour,
    )


def _duration_hours(duration: timedelta) -> Decimal:
    total_seconds = (
        Decimal(duration.days * 86_400)
        + Decimal(duration.seconds)
        + Decimal(duration.microseconds) / Decimal(1_000_000)
    )
    return total_seconds / Decimal(3_600)
