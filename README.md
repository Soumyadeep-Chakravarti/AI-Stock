# AI-Stock

AI-Stock is a Python backend for retrieving, normalizing, and analyzing market data. It is a ground-up rewrite of an older stock-market project, designed as a modular, typed, and testable foundation for clients such as the rebuilt StockAlgo frontend.

## Status

**Early development.**

The current implementation establishes the backend foundation before market-data providers and analysis features are added.

Implemented so far:

- HTTP request and response abstractions
- Pluggable network client interface
- `urllib`-based network client
- Query parameter handling
- HTTP and transport error handling
- Automated network tests
- Strict static type checking
- Reproducible Python and Nix development environment

## Albion Online Testbed

AI-Stock is intended to be a general market-analysis backend, but its first real implementation target is Albion Online's player-driven economy. Albion is not a simulation of a stock market. It is a distinct, real market with buyers, sellers, regional prices, transaction volume, bid and ask spreads, arbitrage opportunities, and economic consequences.

This makes it a controlled environment with an actual use case for developing and validating market-analysis infrastructure before applying it to financial markets. For example, a regional arbitrage recommendation can be executed in Albion and compared with its expected margin.

The Albion provider will translate game-specific data into normalized market data. The analysis layer must not depend on whether an instrument is an Albion item or a financial asset.

```text
                 AI-Stock
                    |
           Generic market models
                    |
          Analysis and strategies
                    |
             Provider API
             /            \
            v              v
     Albion provider   Financial providers
            |              |
            v              v
     Albion economy    NSE / NYSE / ...
            |
            v
      First testbed
```

Potential Albion validation work includes price-movement prediction, spread and liquidity analysis, regional arbitrage, volatility and volume signals, portfolio allocation, risk-adjusted returns, and backtesting against forward results. Mistakes in this testbed do not involve real-world financial capital.

## Architecture

The backend is built in layers:

```text
StockAlgo and other clients
            |
            v
    Application layer
            |
            v
  Analysis and services
            |
            v
        Providers
            |
            v
     Network layer
            |
            v
 External market APIs
```

Provider-specific API formats remain isolated from the rest of the application. The network layer handles HTTP transport and raw bytes; providers parse and normalize external data; analysis operates on normalized market models.

## Project Structure

```text
AI-Stock/
|-- .nix/
|   |-- flake.lock
|   `-- flake.nix
|-- src/
|   `-- ai_stock/
|       |-- network/
|       |   |-- client.py
|       |   |-- errors.py
|       |   |-- types.py
|       |   `-- urllib_client.py
|       |-- __init__.py
|       `-- types.py
|-- tests/
|   `-- network/
|       `-- test_urllib_client.py
|-- .envrc
|-- .python-version
|-- pyproject.toml
`-- uv.lock
```

## Requirements

- Python 3.14+
- `uv`

Nix users can use the included development environment.

## Development Setup

```bash
git clone <repository-url>
cd AI-Stock
uv sync
```

For Nix with direnv:

```bash
direnv allow
```

## Development Commands

Run tests:

```bash
uv run pytest -v
```

Run type checking:

```bash
uv run basedpyright
```

Run linting and formatting:

```bash
uv run ruff format .
uv run ruff check .
```

Run the complete local quality check:

```bash
uv run ruff format . && uv run ruff check . && uv run basedpyright && uv run pytest -v
```

## Network Layer

The network layer deliberately provides a small transport abstraction:

```text
HttpRequest
     |
     v
NetworkClient
     |
     v
UrllibNetworkClient
     |
     v
HttpResponse
```

`NetworkClient` is a protocol, so higher-level components can depend on the abstraction rather than `urllib`. The current client supports GET, POST, PUT, PATCH, DELETE, request headers, query parameters, request bodies, HTTP error responses, and transport failure abstraction.

The network layer intentionally does not parse JSON or understand market data. It only transports requests and responses.

## Testing

Network tests use a local HTTP server and do not depend on external services. The suite verifies basic GET requests, query parameter encoding, preservation of existing query parameters, POST methods and bodies, HTTP error responses, and transport failures.

## Planned Development

```text
Network foundation
        |
        v
Provider abstraction
        |
        v
Albion market-data provider
        |
        v
Normalized market models
        |
        v
Analysis services and strategies
        |
        v
Financial market providers
        |
        v
Application interfaces
```

## Design Principles

- Keep dependencies minimal.
- Prefer standard-library functionality where practical.
- Maintain strict type checking.
- Keep external API details inside provider implementations.
- Keep transport independent of serialization and domain logic.
- Test infrastructure before building features on top of it.
- Keep the backend independent of frontend concerns.
- Prefer explicit interfaces over tightly coupled implementations.

## License

Licensing for the rewritten project has not yet been defined.
