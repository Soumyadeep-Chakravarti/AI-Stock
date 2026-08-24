# Albion Provider Overview

The Albion provider is AI-Stock's first external market implementation. It uses the Albion Online Data Project REST API and translates its response schemas into generic market observations.

```text
Albion API
    |
    v
AlbionMarketDataClient
    |
    v
Albion parser and schema types
    |
    v
CurrentPriceObservation / HistoricalPriceObservation
```

Albion item IDs, qualities, locations, endpoint paths, and response field names are provider concerns. Analysis receives only generic IDs and observations.

The initial REST implementation is intentionally separate from the project's NATS streams. Streaming has replay and missed-message concerns and is a later ingestion subsystem.
