from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from ai_stock.market.types import CurrentPriceObservation, InstrumentId, MarketId


@dataclass(frozen=True, slots=True)
class ArbitrageOpportunity:
    """A gross cross-market opportunity before costs and freshness checks."""

    instrument_id: InstrumentId
    buy_market_id: MarketId
    sell_market_id: MarketId
    buy_price: Decimal
    sell_price: Decimal
    gross_profit: Decimal
    gross_return_percentage: Decimal


def find_arbitrage_opportunities(
    observations: Sequence[CurrentPriceObservation],
) -> Sequence[ArbitrageOpportunity]:
    opportunities: list[ArbitrageOpportunity] = []

    for buy_observation in observations:
        if buy_observation.ask_price is None:
            continue

        for sell_observation in observations:
            if (
                sell_observation.instrument_id != buy_observation.instrument_id
                or sell_observation.market_id == buy_observation.market_id
                or sell_observation.bid_price is None
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
                    sell_price=sell_observation.bid_price,
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
