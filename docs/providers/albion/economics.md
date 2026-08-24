# Albion Instant-Execution Economics

The first net-economics policy models immediate execution only:

```text
buy existing ask
        |
        v
sell into existing bid
        |
        v
market tax on sale
```

The default `AlbionMarketFeePolicy` is non-Premium with no setup fee. It applies an 8% sale tax:

```text
sale_tax   = sell_price * 0.08
net_revenue = sell_price - sale_tax
net_profit  = net_revenue - buy_price
net_return  = net_profit / buy_price * 100
```

Premium is configurable and reduces the market tax by 50%, producing a 4% rate. The first baseline remains non-Premium.

Setup fees are explicitly rejected by the instant-execution calculator. They belong to a later order-based strategy, where the system creates or changes buy/sell orders instead of directly taking existing orders.

## Rounding

The engine intentionally preserves exact `Decimal` arithmetic and does not quantize tax. Albion prices are integer silver, but the authoritative in-game rounding stage and direction have not yet been verified empirically. Reproduce integer rounding only after that behavior is measured and documented.

Manual transport inputs can now adjust a net opportunity for quantity, capacity, and complete cycle time. See [transport economics](transport.md). Route risk, loss probability, capacity by item weight, slippage, and execution probability remain outside v1.
