# Statistics

`analysis.statistics` provides pure functions over `HistoricalPriceObservation` sequences:

- Arithmetic mean price.
- Absolute price change.
- Percentage price change.
- Population price volatility.
- Sample price volatility.

All calculations use `Decimal`. Change functions use chronological order determined by `observed_at`, not caller order.

Population volatility divides variance by `n`; sample volatility divides by `n - 1` and requires at least two observations. Empty series are rejected, and percentage change rejects a zero starting price.

The module knows nothing about Albion, item quality, city names, HTTP, or persistence.
