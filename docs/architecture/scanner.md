# Scanner

The scanner is an application/use-case layer, not an analysis module. It composes a current-price client with generic arbitrage analysis:

```text
fetch observations
       |
       v
detect gross opportunities
       |
       v
apply freshness policy
       |
       v
calculate quote diagnostics and coverage
       |
       v
ArbitrageScanResult
```

`ArbitrageScanResult` contains:

- `opportunities`: ranked, freshness-filtered gross opportunities.
- `quote_statuses`: presence, age, and freshness for each quote side.
- `coverage`: per-instrument market and side-coverage aggregates.

The scanner accepts its freshness thresholds from the caller. It does not hard-code regional policy, fees, travel, or transport economics.
