# Analysis

Analysis functions consume generic market observations only. They do not import Albion modules, call HTTP clients, or persist data.

The current analysis primitives are:

- Mean historical price.
- Absolute and percentage historical price change.
- Population and sample volatility.
- Gross cross-market arbitrage detection.
- Opportunity freshness filtering.

All monetary calculations use `Decimal`. Historical change functions sort observations chronologically rather than trusting input order.

This boundary is an architectural test: the same functions must work for an Albion item, a financial instrument, or a future provider without conditionals for source identity.
