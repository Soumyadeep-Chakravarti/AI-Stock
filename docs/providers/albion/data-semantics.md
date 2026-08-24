# Albion Data Semantics

The provider is the semantic translation boundary.

```text
Albion item_id       -> InstrumentId
Albion city/location -> MarketId
Albion quality       -> provider request/schema concern
```

Quality does not currently enter the generic market model. Callers must scope queries deliberately and should not mix quality variants under the same opaque generic instrument identity without a future identity policy.

## Timestamps

Albion REST timestamps are naive ISO strings. The provider interprets them as UTC and produces UTC-aware `datetime` values. This is required for quote-age and timestamp-skew calculations.

## Historical Quantity

```text
Albion item_count -> HistoricalPriceObservation.quantity
Albion avg_price  -> HistoricalPriceObservation.price
```

`item_count` represents the source-reported aggregate item amount for a historical sell-order bucket. It is not confirmed executed-trade volume. Consumers must not silently reinterpret `quantity` as exchange volume.

## Schema Failures

Malformed Albion JSON, unexpected value types, and missing required fields are normalized as `AlbionParseError`. Raw `KeyError` and JSON implementation details do not escape the parser boundary.
