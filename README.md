# AI-Stock

AI-Stock is a Python backend for retrieving, normalizing, and analyzing market data. It is a ground-up rewrite of an older stock-market project, designed as a modular, typed, and testable foundation for clients such as the rebuilt StockAlgo frontend.

## Status

**Early development.**

The backend has a working Albion Online REST provider, generic historical statistics, gross cross-market arbitrage analysis, freshness policy, scan diagnostics, and live-validation experiments. It remains intentionally small: net costs, transport economics, persistence, streaming ingestion, and machine learning are not implemented.

## Albion First

Albion Online is the first real testbed for AI-Stock's generic market architecture. It is not a stock-market simulation. Its player-driven economy provides real bid/ask spreads, regional markets, historical aggregates, and outcomes that can be checked in-game without risking real financial capital.

```text
Albion API -> Albion provider -> generic observations -> analysis/scanner
```

The provider translates Albion-specific item IDs, quality, locations, and JSON schema before data reaches generic analysis. Future financial sources should follow the same boundary.

## Documentation

- [Architecture overview](docs/architecture/overview.md)
- [Market model](docs/architecture/market-model.md)
- [Networking](docs/architecture/networking.md)
- [Provider boundary](docs/architecture/providers.md)
- [Analysis](docs/architecture/analysis.md)
- [Scanner](docs/architecture/scanner.md)
- [Albion provider](docs/providers/albion/overview.md)
- [Albion data semantics](docs/providers/albion/data-semantics.md)
- [Albion instant-execution economics](docs/providers/albion/economics.md)
- [Gross arbitrage](docs/analysis/arbitrage.md)
- [Freshness policy](docs/analysis/freshness.md)
- [Albion experiment methodology](docs/experiments/albion/methodology.md)
- [Freshness policy experiment](docs/experiments/albion/freshness-policy.md)
- [Instant-execution net economics experiment](docs/experiments/albion/net-economics.md)
- [Development conventions](docs/development/conventions.md)

## Architecture

The active dependency direction is:

```text
External source -> Network -> Provider -> Generic market observations
                                             |              |
                                             v              v
                                         Analysis         Scanner
```

`analysis` imports generic market types only. Provider-specific API details remain inside `providers`.

## Project Structure

```text
AI-Stock/
|-- .nix/
|   |-- flake.lock
|   `-- flake.nix
|-- src/
|   `-- ai_stock/
|       |-- analysis/
|       |-- market/
|       |-- network/
|       |-- providers/albion/
|       `-- scanner/
|-- tests/
|-- docs/
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

## Current Experiment Finding

On an observed 50-item Albion Asia snapshot, quote coverage plateaued at a 24-hour maximum age. Timestamp skew controlled confidence rather than source-side coverage: qualifying gross opportunities rose from 43 at 30-minute skew to 91 without a skew limit. These are provisional observed policies, not global constants. See the [freshness policy study](docs/experiments/albion/freshness-policy.md).

## License

Licensing for the rewritten project has not yet been defined.
