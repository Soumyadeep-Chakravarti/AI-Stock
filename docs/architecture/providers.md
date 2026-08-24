# Providers

Providers convert external market systems into generic observations. A provider owns:

- Endpoint paths and request parameters.
- Source-specific identifiers and variants.
- Raw response schema types.
- Parsing and validation.
- Translation into `CurrentPriceObservation` and `HistoricalPriceObservation`.

```text
Source JSON
    |
    v
Provider schema types
    |
    v
Provider parser
    |
    v
Generic market observations
```

The `MarketDataProvider` protocol describes the intended generic read boundary. Source-specific clients may expose additional controls where their API has real constraints, such as Albion's discrete historical intervals.

Providers must not let source names or schema fields leak into generic analysis.
