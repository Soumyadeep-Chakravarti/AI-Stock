# Architecture Overview

AI-Stock is a layered market-analysis backend. External sources are translated into generic observations before any analysis is performed.

```text
External market source
        |
        v
     Network
        |
        v
     Provider
        |
        v
Generic market observations
        |
        +-----------------+
        v                 v
    Analysis          Scanner
        |                 |
        +--------+--------+
                 v
      Application clients
```

The first real provider is Albion Online. It is a proving ground for the generic model, not an exception to it. Future financial providers should feed the same market and analysis layers.

## Dependency Rules

- `network` has no market-domain semantics.
- `market` has no provider dependency.
- `providers` depend on `network` and `market`.
- `analysis` depends only on `market`.
- `scanner` orchestrates provider-facing clients and generic analysis.
- Provider-specific identifiers, API schemas, and parsing must not reach `analysis`.

These rules prevent an Albion item, a stock ticker, or a provider response shape from becoming an accidental core-domain concept.
