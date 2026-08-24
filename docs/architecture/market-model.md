# Market Model

The current model contains only concepts justified by both Albion and potential financial sources.

## Identifiers

- `InstrumentId`: an opaque identifier for something priced in a market.
- `MarketId`: an opaque identifier for the market where a quote is observed.

Neither type assumes an equity, company, exchange, or game item.

## Current Prices

`CurrentPriceObservation` contains an instrument, a market, and independent bid and ask sides:

```text
bid_price, bid_observed_at
ask_price, ask_observed_at
```

The timestamps remain separate because a buy decision uses the ask timestamp and a sell decision uses the bid timestamp. Combining them would hide temporal risk.

## Historical Prices

`HistoricalPriceObservation` contains:

```text
instrument_id
market_id
price
observed_at
quantity
```

`quantity` is source-reported aggregate quantity. It is not universally equivalent to completed-trade volume.

## Deliberately Absent Concepts

The model does not yet claim to support `Stock`, `Ticker`, `Company`, `Exchange`, `OHLC`, `Trade`, or `OrderBook`. Those concepts need source semantics that the current providers do not establish.
