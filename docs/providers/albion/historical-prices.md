# Albion Historical Prices

`AlbionMarketDataClient.get_historical_prices()` requests grouped history records and flattens every source point into a `HistoricalPriceObservation`.

Albion supports only discrete history buckets:

```text
AlbionHistoryInterval.HOUR       = 1
AlbionHistoryInterval.SIX_HOURS  = 6
AlbionHistoryInterval.DAY        = 24
```

The client validates the requested interval instead of claiming support for arbitrary periods such as 15 minutes.

Each source group is identified by item, location, and quality. Its `data` array is flattened so each historical point carries the generic instrument and market identifiers with its price, timestamp, and quantity.

The REST history endpoint is sell-order-only aggregation. It does not provide a generic candle, bid history, full order book, or confirmed individual trades.
