# Current Liquidity Availability Study

The Asia current-price endpoint was queried for `T4_BAG` in Bridgewatch:

```text
GET /api/v2/stats/prices/T4_BAG.json?locations=Bridgewatch
```

Each returned record contained item identity, location, quality, minimum and maximum sell prices, maximum and minimum buy prices, and a timestamp for each price. It did not contain an order quantity, cumulative depth, or any other quantity associated with a current bid or ask.

The historical endpoint returned `item_count`, `avg_price`, and `timestamp` per bucket. `item_count` is an aggregate historical sell-order amount. It cannot establish how many items remain available at the current lowest ask, or how much can execute at the current highest bid.

## Decision

The Albion Data Project REST endpoints currently used by this project cannot support quantity-constrained immediate execution. Do not infer executable quantity from historical `item_count`, and do not allow transport capacity or requested quantity to imply that a quoted price applies to the entire load.

Quantity-constrained sizing remains blocked until a source supplies current order-side quantity or depth with clear semantics. Historical volume may later be used as a separate liquidity-confidence signal, but not as executable depth.
