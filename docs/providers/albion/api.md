# Albion REST API

The provider uses the Albion Online Data Project regional hosts:

- Americas: `https://west.albion-online-data.com`
- Asia: `https://east.albion-online-data.com`
- Europe: `https://europe.albion-online-data.com`

## Endpoints

```text
/api/v2/stats/prices/{item_ids}.json
/api/v2/stats/history/{item_ids}.json
```

Both endpoints accept comma-separated item IDs, locations, and qualities. History also accepts `date`, `end_date`, and `time-scale`.

The source documents limits of 180 requests per minute and 300 requests per five minutes. Clients should batch requested item/location combinations where possible and use compression for sustained workloads.

API availability is not part of the unit-test contract. Live requests belong to experiments or application execution, not CI.
