# Freshness Policy

Gross profitability and evidence quality are separate concerns. Detection creates gross opportunities first; freshness filtering applies caller-supplied policy afterwards.

For a buy ask timestamp `t_ask`, sell bid timestamp `t_bid`, and evaluation time `now`:

```text
buy_quote_age  = now - t_ask
sell_quote_age = now - t_bid
timestamp_skew = |t_ask - t_bid|
```

Quote age answers: "How old is this evidence?" Timestamp skew answers: "How contemporaneous are the two legs?" A pair can contain two individually recent quotes that are still too far apart in time to trust as a spread.

`filter_fresh_opportunities()` accepts:

- `max_quote_age`, required for both legs.
- `max_timestamp_skew`, optional for temporal comparability.

The Albion Asia experiments found that these knobs control different outcomes. At a 24-hour age policy, relaxing skew from 30 minutes to unlimited increased qualifying gross opportunities from 43 to 91 while source-side coverage did not change.

For the observed Asia sample, 24 hours is a provisional empirical quote-age default. It is not a universal Albion or AI-Stock constant. Timestamp skew remains a tunable confidence policy.
