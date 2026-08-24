# AI-Stock Roadmap

## Next: Liquidity And Sizing

- Investigate which Albion source can provide available quantity at the quoted bid and ask prices.
- Define quantity-constrained opportunity sizing from observed liquidity.
- Prevent transport calculations from assuming a requested quantity can execute at one quoted price.

## Transport Evidence

- Record measured complete-cycle times for real Albion routes, mounts, and loadouts.
- Design an empirical `RouteProfile` only after enough route samples exist.
- Evaluate item-weight capacity once the required source and player inputs are defined.

## Economics

- Verify Albion's integer-silver market-tax rounding behavior in-game before quantizing `Decimal` tax calculations.
- Add order-based execution economics separately: setup fees plus market tax.
- Keep Premium as a configurable policy and compare it with the non-Premium baseline.

## Risk And Execution

- Model route danger and loss probability only after deterministic transport and liquidity sizing are validated.
- Add slippage and execution-probability assumptions only when source data can support them.
- Do not treat a gross, net, or transport-adjusted result as a guaranteed executable trade.

## Providers And Data

- Compare coverage, freshness, and skew behavior across Albion regions.
- Consider streaming ingestion only after REST coverage and persistence requirements are understood.
- Add financial providers only when their source semantics justify extensions to the generic market model.
