# Gross Arbitrage

The detector compares a buy market's ask with a different sell market's bid for the same instrument.

```text
gross_profit = sell_bid - buy_ask
gross_return_percentage = (sell_bid - buy_ask) / buy_ask * 100
```

An `ArbitrageOpportunity` is evidence of a gross cross-market price discrepancy, not a guarantee of realizable profit.

## Detector Invariants

- Buy ask is present and greater than zero.
- Sell bid is present and greater than zero.
- Both quotes belong to the same instrument.
- Buy and sell markets differ.
- Sell bid exceeds buy ask.
- The buy ask and sell bid both have timestamps.

Opportunities are ranked by gross profit. They retain their buy and sell timestamps and expose derived `buy_quote_age`, `sell_quote_age`, and `timestamp_skew` diagnostics.

## Excluded Economics

The detector itself does not model costs. Albion's separate immediate-execution economics policy currently applies market tax only; listing/setup fees, transport cost, travel time, capacity, route risk, slippage, execution probability, and price movement during transport remain outside the model.
