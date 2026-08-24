from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from ai_stock.analysis.arbitrage import ArbitrageOpportunity

NON_PREMIUM_MARKET_TAX_RATE = Decimal("0.08")


@dataclass(frozen=True, slots=True)
class AlbionMarketFeePolicy:
    """Fee policy for an immediate market execution."""

    premium: bool = False
    include_setup_fee: bool = False

    @property
    def market_tax_rate(self) -> Decimal:
        if self.premium:
            return NON_PREMIUM_MARKET_TAX_RATE / Decimal(2)
        return NON_PREMIUM_MARKET_TAX_RATE


DEFAULT_INSTANT_EXECUTION_FEE_POLICY = AlbionMarketFeePolicy()


@dataclass(frozen=True, slots=True)
class AlbionNetArbitrageOpportunity:
    gross_opportunity: ArbitrageOpportunity
    sale_tax: Decimal
    net_revenue: Decimal
    net_profit: Decimal
    net_return_percentage: Decimal


def calculate_net_arbitrage(
    opportunity: ArbitrageOpportunity,
    policy: AlbionMarketFeePolicy = DEFAULT_INSTANT_EXECUTION_FEE_POLICY,
) -> AlbionNetArbitrageOpportunity:
    if policy.include_setup_fee:
        raise ValueError("Setup fees require an order-based execution model")

    sale_tax = opportunity.sell_price * policy.market_tax_rate
    net_revenue = opportunity.sell_price - sale_tax
    net_profit = net_revenue - opportunity.buy_price

    return AlbionNetArbitrageOpportunity(
        gross_opportunity=opportunity,
        sale_tax=sale_tax,
        net_revenue=net_revenue,
        net_profit=net_profit,
        net_return_percentage=net_profit / opportunity.buy_price * Decimal(100),
    )


def find_profitable_net_arbitrage(
    opportunities: Sequence[ArbitrageOpportunity],
    policy: AlbionMarketFeePolicy = DEFAULT_INSTANT_EXECUTION_FEE_POLICY,
) -> Sequence[AlbionNetArbitrageOpportunity]:
    net_opportunities = tuple(
        calculate_net_arbitrage(opportunity, policy) for opportunity in opportunities
    )
    return tuple(
        sorted(
            (
                opportunity
                for opportunity in net_opportunities
                if opportunity.net_profit > 0
            ),
            key=lambda opportunity: opportunity.net_profit,
            reverse=True,
        )
    )
