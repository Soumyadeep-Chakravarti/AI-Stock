# AI-Stock Roadmap

## Next: Liquidity And Sizing

- The current Albion Data Project REST source does not provide available quantity at its quoted bid or ask prices. See the [liquidity availability study](docs/experiments/albion/liquidity-availability.md).
- Identify a source that provides current order-side quantity or depth with clear semantics.
- Define quantity-constrained opportunity sizing only from observed executable liquidity.
- Keep transport calculations from assuming a requested quantity can execute at one quoted price.

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
