# Albion Current Prices

`AlbionMarketDataClient.get_current_prices()` requests current market records for explicit Albion item IDs, locations, and qualities.

The parser maps the best available sides as follows:

```text
Albion buy_price_max       -> generic bid_price
Albion buy_price_max_date  -> generic bid_observed_at

Albion sell_price_min      -> generic ask_price
Albion sell_price_min_date -> generic ask_observed_at
```

Each side is retained independently. A market may have a current ask and no bid, or the reverse.

Albion uses zero-valued prices to represent a missing quote. The parser maps a non-positive source price to `None` and discards its sentinel timestamp. Generic arbitrage analysis independently rejects missing and non-positive sides as a defensive boundary.

Current-price observations are snapshots, not an order book or a record of completed trades.
